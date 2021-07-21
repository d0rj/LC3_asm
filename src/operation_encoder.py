from typing import List

from .typechecking import required_argument_types, arguments_matched_any
from .utils.lc3_constants import Operations, Registers, TokenType as TT
from .utils.argument import Argument


class OperationEncoder:
	__slots__ = '_operations', '_registers'


	def __init__(self) -> None:
		self._operations = Operations(0)
		self._registers = Registers(0)


	def NOT(self, arguments: List[Argument]) -> int:
		required_argument_types(arguments, [TT.REGISTER_NAME, TT.REGISTER_NAME], 'not')

		dst = int(self._registers[str(arguments[0].value)]) & 0b111
		src = int(self._registers[str(arguments[1].value)]) & 0b111

		result = int(self._operations['not']) << 12 | dst << 9 | src << 6 | 0b111111
		return result


	def _and_add_base(self, arguments: List[Argument], op_name: str) -> int:
		rule, message = arguments_matched_any(
			arguments,
			[
				[TT.REGISTER_NAME, TT.REGISTER_NAME, TT.REGISTER_NAME],
				[TT.REGISTER_NAME, TT.REGISTER_NAME, TT.NUMBER]
			],
			op_name
		)

		if rule == 0:
			dst = int(self._registers[str(arguments[0].value)]) & 0b111
			src1 = int(self._registers[str(arguments[1].value)]) & 0b111
			src2 = int(self._registers[str(arguments[2].value)]) & 0b111

			result = int(self._operations[op_name]) << 12 | dst << 9 | src1 << 6 | 0b000 << 3 | src2
		elif rule == 1:
			dst = int(self._registers[str(arguments[0].value)]) & 0b111
			src1 = int(self._registers[str(arguments[1].value)]) & 0b111
			imm5 = int(arguments[2].value) & 0b11111

			result = int(self._operations[op_name]) << 12 | dst << 9 | src1 << 6 | 0b1 << 5 | imm5
		else:
			raise SyntaxError(message)

		return result


	def _register_pcoffset9_base(self, arguments: List[Argument], op_name: str) -> int:
		required_argument_types(arguments, [TT.REGISTER_NAME, TT.NUMBER], op_name)

		dst = int(self._registers[str(arguments[0].value)]) & 0b111
		pc_offset = int(arguments[1].value) & 0xf

		result = int(self._operations[op_name]) << 12 | dst << 9 | pc_offset
		return result


	def _register_base_offset_base(self, arguments: List[Argument], op_name: str) -> int:
		required_argument_types(arguments, [TT.REGISTER_NAME, TT.REGISTER_NAME, TT.NUMBER], op_name)

		dst = int(self._registers[str(arguments[0].value)]) & 0b111
		base = int(self._registers[str(arguments[1].value)]) & 0b111
		offset6 = int(arguments[2].value) & 0b111111

		result = int(self._operations[op_name]) << 12 | dst << 9 | base << 6 | offset6
		return result


	def _base_BR(self, arguments: List[Argument], op_name: str) -> int:
		required_argument_types(arguments, [TT.NUMBER], op_name)

		pc_offset9 = int(arguments[0].value) & 0x1ff

		result = int(self._operations[op_name]) << 9 | pc_offset9
		return result


	def _trap_subops_base(self, arguments: List[Argument], op_name: str) -> int:
		required_argument_types(arguments, [], op_name)

		return self._operations[op_name]


	def ADD(self, arguments: List[Argument]) -> int:
		return self._and_add_base(arguments, 'add')


	def AND(self, arguments: List[Argument]) -> int:
		return self._and_add_base(arguments, 'and')


	def LD(self, arguments: List[Argument]) -> int:
		return self._register_pcoffset9_base(arguments, 'ld')


	def ST(self, arguments: List[Argument]) -> int:
		return self._register_pcoffset9_base(arguments, 'st')


	def LDI(self, arguments: List[Argument]) -> int:
		return self._register_pcoffset9_base(arguments, 'ldi')


	def STI(self, arguments: List[Argument]) -> int:
		return self._register_pcoffset9_base(arguments, 'sti')


	def LDR(self, arguments: List[Argument]) -> int:
		return self._register_base_offset_base(arguments, 'ldr')


	def STR(self, arguments: List[Argument]) -> int:
		return self._register_base_offset_base(arguments, 'str')


	def LEA(self, arguments: List[Argument]) -> int:
		return self._register_pcoffset9_base(arguments, 'lea')


	def BR(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'br')


	def BRN(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brn')


	def BRZ(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brz')


	def BRP(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brp')


	def BRNZ(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brnz')


	def BRNP(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brnp')


	def BRZP(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brzp')


	def BRZNP(self, arguments: List[Argument]) -> int:
		return self._base_BR(arguments, 'brznp')


	def JMP(self, arguments: List[Argument]) -> int:
		required_argument_types(arguments, [TT.REGISTER_NAME], 'jmp')

		base = int(self._registers[str(arguments[0].value)]) & 0b111

		result = int(self._operations['jmp']) << 12 | base << 6
		return result


	def TRAP(self, arguments: List[Argument]) -> int:
		required_argument_types(arguments, [TT.NUMBER], 'trap')

		trapvect = int(arguments[0].value) & 0xff

		result = int(self._operations['trap']) << 12 | trapvect
		return result


	def GETC(self, arguments: List[Argument]) -> int:
		return self._trap_subops_base(arguments, 'getc')


	def OUT(self, arguments: List[Argument]) -> int:
		return self._trap_subops_base(arguments, 'out')


	def PUTS(self, arguments: List[Argument]) -> int:
		return self._trap_subops_base(arguments, 'puts')


	def IN(self, arguments: List[Argument]) -> int:
		return self._trap_subops_base(arguments, 'in')


	def PUTSP(self, arguments: List[Argument]) -> int:
		return self._trap_subops_base(arguments, 'putsp')


	def HALT(self, arguments: List[Argument]) -> int:
		return self._trap_subops_base(arguments, 'halt')


	def __getitem__(self, name: str):
		return getattr(self, name.upper())
