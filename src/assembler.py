from os import error
from lark import Tree

from typing import Dict, List


MEMORY_SIZE = 65535

HEX_NUMBER = 'hex_number'
BIN_NUMBER = 'bin_number'
DEC_NUMBER = 'dec_number'

PSEUDO_OP = 'pseudo_op'
ORIG = '.orig'
FILL = '.fill'

LABEL = 'label'
INSTRUCTION = 'instruction'


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
	return args[0] if len(args) > 0 else []


def _argument_type(tree: Tree) -> tuple:
	argument_type = tree.children[0].data
	return argument_type, tree.children[0]


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


def preprocess(tree: Tree):
	global _labels, _memory
	
	current_address = 0

	commands: List[Tree] = tree.children
	commands = [c.children[0] for c in commands] # eat a 'command' ast node

	instructions: Dict[int, Tree] = dict()

	for command in commands: # find all labels
		if command.data == INSTRUCTION:
			instructions[current_address] = command
		elif command.data == LABEL:
			_labels[_extract_label_name(command)] = current_address
			current_address -= 1
		elif _is_orig_command(command):
			orig_arguments = _get_arguments_tree(command)
			if len(orig_arguments) != 1:
				raise SyntaxError(f'\'.ORIG\' instruction must have one argument, but {len(orig_arguments)} was given.')

			arg_type, arg = _argument_type(orig_arguments[0])
			if arg_type != 'number':
				raise SyntaxError(f'\'.ORIG\' instruction argument must have type of number, but {arg_type} was given.')

			current_address = _number_tree_to_int(arg) - 1
		elif _is_fill_command(command):
			fill_arguments = _get_arguments_tree(command)
			if len(fill_arguments) != 1:
				raise SyntaxError(f'\'.FILL\' instruction must have one argument, but {len(fill_arguments)} was given.')

			_memory[current_address] = _number_tree_to_int(orig_arguments[0].children[0])
		# TODO: stringz and blkw
		
		current_address += 1

	result: Dict[int, dict]
	for addr, instruction in instructions.items(): # move AST to dict and replace labels with it's values
		print(f'{hex(addr)} - {_get_arguments_tree(instruction)}')
		pass


def assemble(tree: Tree):
	global _labels, _instructions, _memory
	pass


def process(tree: Tree) -> bytearray:
	global _memory

	if tree.data != 'start':
		raise ValueError('Unsupported tree format passed to function. Start node required.')

	preprocess(tree)
	assemble(tree)

	return _memory
