from lark import Tree

from typing import Dict, List, Tuple

from .typechecking import required_argument_types, arguments_matched_any
from .utils.dict_variable import var_name, var_value
from .utils.lc3_constants import Operations, Registers,\
	REGISTER_NAME, NUMBER, LABEL, STRING, INSTRUCTION, MEMORY_SIZE,\
		ORIG, FILL, STRINGZ
from .utils.tree_processing import argument_type, number_tree_to_int, \
	get_arguments_tree, is_fill_command, is_orig_command, is_stringz_command, \
		instruction_name, extract_label_name


class EncodeOperation:
	__slots__ = '_operations', '_registers'


	def __init__(self) -> None:
		self._operations = Operations(0)
		self._registers = Registers(0)


	def NOT(self, arguments: List[Dict]) -> int:
		required_argument_types(arguments, [REGISTER_NAME, REGISTER_NAME], 'not')

		dst = int(self._registers[var_value(arguments[0])]) & 0b111
		src = int(self._registers[var_value(arguments[1])]) & 0b111

		result = int(self._operations['not']) << 12 | dst << 9 | src << 6 | 0b111111
		return result


	def _and_add_base(self, arguments: List[Dict], op_name: str) -> int:
		rule, message = arguments_matched_any(
			arguments,
			[
				[REGISTER_NAME, REGISTER_NAME, REGISTER_NAME],
				[REGISTER_NAME, REGISTER_NAME, NUMBER]
			],
			op_name
		)

		if rule == 0:
			dst = int(self._registers[var_value(arguments[0])]) & 0b111
			src1 = int(self._registers[var_value(arguments[1])]) & 0b111
			src2 = int(self._registers[var_value(arguments[2])]) & 0b111

			result = int(self._operations[op_name]) << 12 | dst << 9 | src1 << 6 | 0b000 << 3 | src2
		elif rule == 1:
			dst = int(self._registers[var_value(arguments[0])]) & 0b111
			src1 = int(self._registers[var_value(arguments[1])]) & 0b111
			imm5 = int(var_value(arguments[2])) & 0b11111

			result = int(self._operations[op_name]) << 12 | dst << 9 | src1 << 6 | 0b1 << 5 | imm5
		else:
			raise SyntaxError(message)

		return result


	def _register_pcoffset9_base(self, arguments: List[Dict], op_name: str) -> int:
		required_argument_types(arguments, [REGISTER_NAME, NUMBER], op_name)

		dst = int(self._registers[var_value(arguments[0])]) & 0b111
		pc_offset = int(var_value(arguments[1])) & 0xf

		result = int(self._operations[op_name]) << 12 | dst << 9 | pc_offset
		return result


	def _register_base_offset_base(self, arguments: List[Dict], op_name: str) -> int:
		required_argument_types(arguments, [REGISTER_NAME, REGISTER_NAME, NUMBER], op_name)

		dst = int(self._registers[var_value(arguments[0])]) & 0b111
		base = int(self._registers[var_value(arguments[1])]) & 0b111
		offset6 = int(var_value(arguments[2])) & 0b111111

		result = int(self._operations[op_name]) << 12 | dst << 9 | base << 6 | offset6
		return result


	def _base_BR(self, arguments: List[Dict], op_name: str) -> int:
		required_argument_types(arguments, [NUMBER], op_name)

		pc_offset9 = int(var_value(arguments[0])) & 0x1ff

		result = int(self._operations[op_name]) << 9 | pc_offset9
		return result


	def _trap_subops_base(self, arguments: List[Dict], op_name: str) -> int:
		required_argument_types(arguments, [], op_name)

		return self._operations[op_name]


	def ADD(self, arguments: List[Dict]) -> int:
		return self._and_add_base(arguments, 'add')


	def AND(self, arguments: List[Dict]) -> int:
		return self._and_add_base(arguments, 'and')


	def LD(self, arguments: List[Dict]) -> int:
		return self._register_pcoffset9_base(arguments, 'ld')


	def ST(self, arguments: List[Dict]) -> int:
		return self._register_pcoffset9_base(arguments, 'st')


	def LDI(self, arguments: List[Dict]) -> int:
		return self._register_pcoffset9_base(arguments, 'ldi')


	def STI(self, arguments: List[Dict]) -> int:
		return self._register_pcoffset9_base(arguments, 'sti')


	def LDR(self, arguments: List[Dict]) -> int:
		return self._register_base_offset_base(arguments, 'ldr')


	def STR(self, arguments: List[Dict]) -> int:
		return self._register_base_offset_base(arguments, 'str')


	def LEA(self, arguments: List[Dict]) -> int:
		return self._register_pcoffset9_base(arguments, 'lea')


	def BR(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'br')


	def BRN(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brn')


	def BRZ(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brz')


	def BRP(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brp')


	def BRNZ(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brnz')


	def BRNP(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brnp')


	def BRZP(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brzp')


	def BRZNP(self, arguments: List[Dict]) -> int:
		return self._base_BR(arguments, 'brznp')


	def JMP(self, arguments: List[Dict]) -> int:
		required_argument_types(arguments, [REGISTER_NAME], 'jmp')

		base = int(self._registers[var_value(arguments[0])]) & 0b111

		result = int(self._operations['jmp']) << 12 | base << 6
		return result


	def TRAP(self, arguments: List[Dict]) -> int:
		required_argument_types(arguments, [NUMBER], 'trap')

		trapvect = int(var_value(arguments[0])) & 0xff

		result = int(self._operations['trap']) << 12 | trapvect
		return result


	def GETC(self, arguments: List[Dict]) -> int:
		return self._trap_subops_base(arguments, 'getc')


	def OUT(self, arguments: List[Dict]) -> int:
		return self._trap_subops_base(arguments, 'out')


	def PUTS(self, arguments: List[Dict]) -> int:
		return self._trap_subops_base(arguments, 'puts')


	def IN(self, arguments: List[Dict]) -> int:
		return self._trap_subops_base(arguments, 'in')


	def PUTSP(self, arguments: List[Dict]) -> int:
		return self._trap_subops_base(arguments, 'putsp')


	def HALT(self, arguments: List[Dict]) -> int:
		return self._trap_subops_base(arguments, 'halt')


	def __getitem__(self, name: str):
		return getattr(self, name.upper())


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
	encode_operation = EncodeOperation()

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
