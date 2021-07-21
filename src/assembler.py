from lark import Tree

from typing import Dict, List, Tuple

from .operation_encoder import OperationEncoder
from .typechecking import required_argument_types
from .asm_code.argument import Argument
from .asm_code.instruction import Instruction
from .utils.lc3_constants import MEMORY_SIZE, TokenType as TT, PseudoOperation as PO
from .utils.tree_processing import instruction_name, extract_label_name, get_arguments_tree


def preprocess(tree: Tree, memory: List[int]) -> Tuple[Dict[int, Instruction], List[int]]:
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
				arguments = [Argument.fromTree(arg_tree) for arg_tree in get_arguments_tree(command)]
				required_argument_types(arguments, [TT.NUMBER], PO.ORIG)
				current_address = int(arguments[0].value) - 1
			elif command == PO.FILL:
				arguments = [Argument.fromTree(arg_tree) for arg_tree in get_arguments_tree(command)]
				required_argument_types(arguments, [TT.NUMBER], PO.FILL)
				memory[current_address] = int(arguments[0].value)
			elif command == PO.STRINGZ:
				arguments = [Argument.fromTree(arg_tree) for arg_tree in get_arguments_tree(command)]
				required_argument_types(arguments, [TT.STRING], PO.STRINGZ)

				string = str(arguments[0].value).replace('"', '')
				_bytes = bytearray(bytes(string, 'ascii'))
				_bytes.append(0x00)
				memory[current_address:(current_address + len(_bytes))] = _bytes
		else:
			raise SyntaxError(f'Unknown command: {command.children[0]}.')

		current_address += 1

	result: Dict[int, Instruction] = dict()
	for addr, instruction in instructions.items():
		name = instruction_name(instruction)
		arguments = [Argument.fromTree(arg_tree) for arg_tree in get_arguments_tree(instruction)]
		# replace labels with address
		arguments = [
			Argument(TT.NUMBER, labels[arg.value])
				if arg.type == TT.LABEL
				else arg
			for arg in arguments
		]

		result[addr] = Instruction(name, arguments)

	return result, memory


def assemble(instructions: Dict[int, Instruction], memory: List[int]) -> List[int]:
	encode_operation = OperationEncoder()

	for addr, instr in instructions.items():
		encoded = encode_operation[instr.name](instr.arguments)
		memory[addr] = encoded

	return memory


def process(tree: Tree) -> list:
	memory = [0 for _ in range(MEMORY_SIZE)]

	if tree.data != 'start':
		raise ValueError('Unsupported tree format passed to function. Start node required.')

	instructions, memory = preprocess(tree, memory)
	memory = assemble(instructions, memory)

	return memory
