from lark import Tree

from typing import Dict, List, Tuple

from .operation_encoder import OperationEncoder
from .typechecking import required_argument_types
from .utils.dict_variable import var_name, var_value, var_from_tree
from .utils.lc3_constants import MEMORY_SIZE, TokenType as TT, PseudoOperation as PO
from .utils.tree_processing import instruction_name, extract_label_name, get_arguments_tree


def preprocess(tree: Tree, memory: List[int]) -> Tuple[Dict[int, Dict[str, list]], List[int]]:
	current_address = 0

	labels: Dict[str, int] = dict()
	commands: List[Tree] = tree.children
	# eat a 'command' ast node
	commands = [c.children[0] for c in commands]

	instructions: Dict[int, Tree] = dict()

	for command in commands:
		if command.data == TT.INSTRUCTION:
			instructions[current_address] = command
		elif command.data == TT.LABEL:
			labels[extract_label_name(command)] = current_address
			current_address -= 1
		elif command.data == TT.PSEUDO_OP:
			if command == PO.ORIG:
				arguments = [var_from_tree(arg_tree) for arg_tree in get_arguments_tree(command)]
				required_argument_types(arguments, [TT.NUMBER], PO.ORIG)
				current_address = var_value(arguments[0]) - 1
			elif command == PO.FILL:
				arguments = [var_from_tree(arg_tree) for arg_tree in get_arguments_tree(command)]
				required_argument_types(arguments, [TT.NUMBER], PO.FILL)
				memory[current_address] = var_value(arguments[0])
			elif command == PO.STRINGZ:
				arguments = [var_from_tree(arg_tree) for arg_tree in get_arguments_tree(command)]
				required_argument_types(arguments, [TT.STRING], PO.STRINGZ)

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
		arguments = [var_from_tree(arg_tree) for arg_tree in get_arguments_tree(instruction)]
		# replace labels with address
		arguments = [
			{ 'number': labels[var_value(arg)] }
				if var_name(arg) == TT.LABEL
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
