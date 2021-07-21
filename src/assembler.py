from lark import Tree

from typing import Dict, List, Tuple

from .operation_encoder import OperationEncoder
from .typechecking import required_argument_types
from .utils.dict_variable import var_name, var_value
from .utils.lc3_constants import REGISTER_NAME, NUMBER, LABEL, STRING, INSTRUCTION, MEMORY_SIZE,\
	ORIG, FILL, STRINGZ
from .utils.tree_processing import argument_type, number_tree_to_int, \
	get_arguments_tree, is_fill_command, is_orig_command, is_stringz_command, \
		instruction_name, extract_label_name


def _argument_tree_parse(argument: Tree) -> dict:
	arg_type = argument_type(argument)

	if arg_type == NUMBER:
		return { NUMBER: number_tree_to_int(argument) }
	if arg_type == REGISTER_NAME:
		return { REGISTER_NAME: str(argument.children[0]) }
	if arg_type == LABEL:
		return { LABEL: str(argument.children[0]) }
	if arg_type == STRING:
		return { STRING: str(argument.children[0]) }

	return None


def preprocess(tree: Tree, memory: List[int]) -> Tuple[Dict[int, Dict[str, list]], List[int]]:
	current_address = 0

	labels: Dict[str, int] = dict()
	commands: List[Tree] = tree.children
	# eat a 'command' ast node
	commands = [c.children[0] for c in commands]

	instructions: Dict[int, Tree] = dict()

	for command in commands:
		if command.data == INSTRUCTION:
			instructions[current_address] = command
		elif command.data == LABEL:
			labels[extract_label_name(command)] = current_address
			current_address -= 1
		elif is_orig_command(command):
			arguments = [_argument_tree_parse(arg_tree) for arg_tree in get_arguments_tree(command)]
			required_argument_types(arguments, [NUMBER], ORIG)
			current_address = var_value(arguments[0]) - 1
		elif is_fill_command(command):
			arguments = [_argument_tree_parse(arg_tree) for arg_tree in get_arguments_tree(command)]
			required_argument_types(arguments, [NUMBER], FILL)
			memory[current_address] = var_value(arguments[0])
		elif is_stringz_command(command):
			arguments = [_argument_tree_parse(arg_tree) for arg_tree in get_arguments_tree(command)]
			required_argument_types(arguments, [STRING], STRINGZ)

			string = str(var_value(arguments[0])).replace('"', '')
			_bytes = bytearray(bytes(string, 'ascii'))
			_bytes.append(0x00)
			memory[current_address:(current_address + len(_bytes))] = _bytes
		else:
			raise SyntaxError(f'Unknown command: {command.children[0]}.')

		current_address += 1

	result: Dict[int, Dict[str, list]] = dict()
	for addr, instruction in instructions.items():
		name = instruction_name(instruction)
		arguments = [_argument_tree_parse(arg_tree) for arg_tree in get_arguments_tree(instruction)]
		# replace labels with address
		arguments = [
			{ 'number': labels[var_value(arg)] }
				if var_name(arg) == LABEL
				else arg
			for arg in arguments
		]

		result[addr] = { name: arguments }

	return result, memory


def assemble(instructions: Dict[int, Dict[str, list]], memory: List[int]) -> List[int]:
	encode_operation = OperationEncoder()

	for addr, instr in instructions.items():
		op_name = var_name(instr)
		arguments = var_value(instr)

		encoded = encode_operation[op_name](arguments)
		memory[addr] = encoded

	return memory


def process(tree: Tree) -> list:
	memory = [0 for _ in range(MEMORY_SIZE)]

	if tree.data != 'start':
		raise ValueError('Unsupported tree format passed to function. Start node required.')

	instructions, memory = preprocess(tree, memory)
	memory = assemble(instructions, memory)

	return memory
