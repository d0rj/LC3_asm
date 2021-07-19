from os import error
from lark import Tree

from typing import Dict, List, Tuple
from enum import Enum


class DictEnum(Enum):
	def __getitem__(self, key: str):
		return getattr(self.__class__, key.upper()).value


class Operations(DictEnum):
	BR, ADD, LD, ST, \
	JSR, AND, LDR, STR, \
	RTI, NOT, LDI, STI, \
	JMP, RES, LEA, TRAP = range(16)
	GETC = 0xf0 << 8 | 0x20
	OUT = 0xf0 << 8 | 0x21
	PUTS = 0xf0 << 8 | 0x22
	IN = 0xf0 << 8 | 0x23
	PUTSP = 0xf0 << 8 | 0x24
	HALT = 0xf0 << 8 | 0x25


class Registers(DictEnum):
	R0, R1, R2, R3, R4, R5, R6, R7, \
	PC, COND = range(10)


class EncodeOperation:
	__slots__ = '_operations', '_registers'


	def __init__(self) -> None:
		self._operations = Operations(Operations.ADD)
		self._registers = Registers(Registers.COND)

	
	def NOT(self, arguments: List[Dict]) -> int:
		_required_argument_types(arguments, [REGISTER_NAME, REGISTER_NAME], 'not')

		dst = int(self._registers[_first_value(arguments[0])]) & 0b111
		src = int(self._registers[_first_value(arguments[1])]) & 0b111

		result = int(self._operations['not']) << 12 | dst << 9 | src << 6 | 0b111111

		return result


	def ADD(self, arguments: List[Dict]) -> int:
		rule, message = _arguments_matched_any(
			arguments, 
			[
				[REGISTER_NAME, REGISTER_NAME, REGISTER_NAME],
				[REGISTER_NAME, REGISTER_NAME, NUMBER]
			],
			'add'
		)
			
		if rule == 0:
			dst = int(self._registers[_first_value(arguments[0])]) & 0b111
			src1 = int(self._registers[_first_value(arguments[1])]) & 0b111
			src2 = int(self._registers[_first_value(arguments[2])]) & 0b111

			result = int(self._operations['add']) << 12 | dst << 9 | src1 << 6 | 0b000 << 3 | src2
		elif rule == 1:
			dst = int(self._registers[_first_value(arguments[0])]) & 0b111
			src1 = int(self._registers[_first_value(arguments[1])]) & 0b111
			imm5 = int(_first_value(arguments[2])) & 0b11111

			result = int(self._operations['add']) << 12 | dst << 9 | src1 << 6 | 0b1 << 5 | imm5
		else:
			raise SyntaxError(message)

		return result


	def __getitem__(self, name: str):
		return getattr(EncodeOperation, name.upper())


MEMORY_SIZE = 65535

NUMBER = 'number'
HEX_NUMBER = 'hex_number'
BIN_NUMBER = 'bin_number'
DEC_NUMBER = 'dec_number'

PSEUDO_OP = 'pseudo_op'
ORIG = '.orig'
FILL = '.fill'
STRINGZ = '.stringz'

LABEL = 'label'
INSTRUCTION = 'instruction'
REGISTER_NAME = 'register_name'
STRING = 'string'


def _first_key(var: dict):
	return list(var.keys())[0]


def _first_value(var: dict):
	return list(var.values())[0]


def _extract_label_name(tree: Tree) -> str:
	return str(tree.children[0])


def _is_pseudo_op(tree: Tree) -> bool:
	return tree.data == PSEUDO_OP


def _is_orig_command(tree: Tree) -> bool:
	return True if _is_pseudo_op(tree) and str(tree.children[0]).lower() == ORIG else False


def _is_fill_command(tree: Tree) -> bool:
	return True if _is_pseudo_op(tree) and str(tree.children[0]).lower() == FILL else False


def _is_stringz_command(tree: Tree) -> bool:
	return True if _is_pseudo_op(tree) and str(tree.children[0]).lower() == STRINGZ else False


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
	if number_type == BIN_NUMBER:
		return int(number_str, 2)
	if number_type == DEC_NUMBER:
		return int(number_str)

	raise ValueError('Not a number.')


def _argument_tree_parse(argument: Tree) -> dict:
	arg_type = _argument_type(argument)

	if arg_type == NUMBER:
		return { NUMBER: _number_tree_to_int(argument) }
	if arg_type == REGISTER_NAME:
		return { REGISTER_NAME: str(argument.children[0]) }
	if arg_type == LABEL:
		return { LABEL: str(argument.children[0]) }
	if arg_type == STRING:
		return { STRING: str(argument.children[0]) }

	return None


def _argument_type_missmatch_message(instruction_name: str, required: str) -> str:
	return f'''\'{instruction_name.upper()}\' instruction arguments must have types {required}.'''


def _argument_count_missmatch_message(instruction_name: str, required: int, passed: int) -> str:
	return f'\'{instruction_name.upper()}\' instruction must have {required} arguments, but {passed} was gived.'


def _arguments_matched(arguments: List[dict], types: List[str], instr: str) -> Tuple[bool, str]:
	if len(arguments) != len(types):
		return False, _argument_count_missmatch_message(instr, len(types), len(arguments))

	all_matched = all([_first_key(arg) == _type for arg, _type in zip(arguments, types)])

	if not all_matched:
		return False, _argument_type_missmatch_message(instr, str(types).replace('[', '').replace(']', ''))

	return True, str()


def _arguments_matched_any(arguments: List[dict], types: List[List[str]], instr: str) -> Tuple[int, str]:
	for i, _types in enumerate(types):
		matched, message = _arguments_matched(arguments, _types, instr)
		if matched:
			return i, str()
	
	return -1, message


def _required_argument_types(arguments: List[dict], types: List[str], instr: str):	
	matched, message = _arguments_matched(arguments, types, instr)
	if not matched:
		raise SyntaxError(message)


def preprocess(tree: Tree, memory: bytearray) -> Tuple[Dict[int, Dict[str, list]], bytearray]:
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
			labels[_extract_label_name(command)] = current_address
			current_address -= 1
		elif _is_orig_command(command):
			arguments = [_argument_tree_parse(arg_tree) for arg_tree in _get_arguments_tree(command)]
			_required_argument_types(arguments, [NUMBER], ORIG)
			current_address = _first_value(arguments[0]) - 1
		elif _is_fill_command(command):
			arguments = [_argument_tree_parse(arg_tree) for arg_tree in _get_arguments_tree(command)]
			_required_argument_types(arguments, [NUMBER], FILL)
			memory[current_address] = _first_value(arguments[0])
		elif _is_stringz_command(command):
			arguments = [_argument_tree_parse(arg_tree) for arg_tree in _get_arguments_tree(command)]
			_required_argument_types(arguments, [STRING], STRINGZ)

			string = str(_first_value(arguments[0])).replace('"', '')
			_bytes = bytearray(bytes(string, 'ascii'))
			_bytes.append(0x00)
			memory[current_address:(current_address + len(_bytes))] = _bytes
		else:
			raise SyntaxError(f'Unknown command: {command.children[0]}.')

		current_address += 1

	result: Dict[int, Dict[str, list]] = dict()
	for addr, instruction in instructions.items():
		name = _instruction_name(instruction)
		arguments = [_argument_tree_parse(arg_tree) for arg_tree in _get_arguments_tree(instruction)]
		# replace labels with address
		arguments = [
			{ 'number': labels[_first_value(arg)] } 
				if _first_key(arg) == LABEL 
				else arg 
			for arg in arguments
		]

		result[addr] = { name: arguments }

	return result, memory


def assemble(instructions: Dict[int, Dict[str, list]], memory: bytearray) -> bytearray:
	operations = Operations(Operations.ADD)
	registers = Registers(Registers.COND)
	encode_operation = EncodeOperation()

	for addr, instr in instructions.items():
		print(f'{hex(addr)}: {instr}')

	return memory


def process(tree: Tree) -> bytearray:
	memory = bytearray(MEMORY_SIZE)

	if tree.data != 'start':
		raise ValueError('Unsupported tree format passed to function. Start node required.')

	instructions, memory = preprocess(tree, memory)
	assemble(instructions, memory)

	return memory
