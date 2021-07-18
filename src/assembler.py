from os import error
from lark import Tree

from typing import Dict, List


MEMORY_SIZE = 65535

NUMBER = 'number'
HEX_NUMBER = 'hex_number'
BIN_NUMBER = 'bin_number'
DEC_NUMBER = 'dec_number'

PSEUDO_OP = 'pseudo_op'
ORIG = '.orig'
FILL = '.fill'

LABEL = 'label'
INSTRUCTION = 'instruction'
REGISTER_NAME = 'register_name'


_labels: Dict[str, int] = dict()
_memory = bytearray(MEMORY_SIZE)


def _extract_label_name(tree: Tree) -> str:
	return str(tree.children[0])


def _is_pseudo_op(tree: Tree) -> bool:
	return tree.data == PSEUDO_OP


def _is_orig_command(tree: Tree) -> bool:
	return True if _is_pseudo_op(tree) and str(tree.children[0]).lower() == ORIG else False


def _is_fill_command(tree: Tree) -> bool:
	return True if _is_pseudo_op(tree) and str(tree.children[0]).lower() == FILL else False


def _get_arguments_tree(tree: Tree) -> List[Tree]:
	args = [arg.children for arg in tree.children if isinstance(arg, Tree) and arg.data == 'arguments']
	args = args[0] if len(args) > 0 else []
	args = [arg.children[0] if arg.data == 'argument' else arg for arg in args]
	return args


def _argument_type(tree: Tree) -> str:
	return tree.data


def _instruction_name(tree: Tree) -> str:
	return str(tree.children[0]).lower()


def _number_tree_to_int(tree: Tree) -> int:
	number_type = str(tree.children[0].type).lower()
	number_str = str(tree.children[0])

	if number_type == HEX_NUMBER:
		return int(number_str, 16)
	elif number_type == BIN_NUMBER:
		return int(number_str, 2)
	elif number_type == DEC_NUMBER:
		return int(number_str)
	else:
		raise ValueError('Not a number.')


def _argument_tree_parse(argument: Tree) -> dict:
	arg_type = _argument_type(argument)

	if arg_type == NUMBER:
		return { NUMBER: _number_tree_to_int(argument) }
	elif arg_type == REGISTER_NAME:
		return { REGISTER_NAME: str(argument.children[0]) }
	elif arg_type == LABEL:
		return { LABEL: str(argument.children[0]) }

	return None


def _required_argument_types(arguments: List[Tree], types: List[str] or List[List[str]], instr: str) -> bool:	
	if len(arguments) != len(types):
		raise SyntaxError(f'\'{instr.upper()}\' instruction must have {len(types)} arguments, but {len(arguments)} was given.')

	all_matched = all([_argument_type(arg) == _type for arg, _type in zip(arguments, types)])

	if not all_matched:
		raise SyntaxError(f'''\'{instr.upper()}\' instruction arguments must have types {str(types).replace('[', '').replace(']', '')}.''')


def preprocess(tree: Tree) -> Dict[int, Dict[str, list]]:
	global _labels, _memory
	
	current_address = 0

	commands: List[Tree] = tree.children
	# eat a 'command' ast node
	commands = [c.children[0] for c in commands]

	instructions: Dict[int, Tree] = dict()

	for command in commands:
		if command.data == INSTRUCTION:
			instructions[current_address] = command
		elif command.data == LABEL:
			_labels[_extract_label_name(command)] = current_address
			current_address -= 1
		elif _is_orig_command(command):
			arguments = _get_arguments_tree(command)
			_required_argument_types(arguments, [NUMBER], ORIG)
			current_address = _number_tree_to_int(arguments[0]) - 1
		elif _is_fill_command(command):
			arguments = _get_arguments_tree(command)
			_required_argument_types(arguments, [NUMBER], FILL)
			_memory[current_address] = _number_tree_to_int(arguments[0])
		# TODO: stringz and blkw
		#else:
			#raise SyntaxError(f'Unknown command: {command.children[0]}.')

		current_address += 1

	result: Dict[int, Dict[str, list]] = dict()
	# move AST to dict and replace labels with it's values
	for addr, instruction in instructions.items():
		name = _instruction_name(instruction)
		arguments = [_argument_tree_parse(arg_tree) for arg_tree in _get_arguments_tree(instruction)]
		# replace labels with address
		arguments = [
			{ 'number': _labels[list(arg.values())[0]] } 
				if list(arg.keys())[0] == LABEL 
				else arg 
			for arg in arguments
		]

		result[addr] = { name: arguments }

	return result


def assemble(instructions: Dict[int, Dict[str, list]]):
	global _labels, _memory

	for addr, instr in instructions.items():
		print(f'{hex(addr)}: {instr}')

	print(_memory[0x3008])
	for label, addr in _labels.items():
		print(f'{label}: {hex(addr)}')


def process(tree: Tree) -> bytearray:
	global _memory

	if tree.data != 'start':
		raise ValueError('Unsupported tree format passed to function. Start node required.')

	instructions = preprocess(tree)
	assemble(instructions)

	return _memory
