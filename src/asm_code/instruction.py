from typing import List

from .argument import Argument


class Instruction:
	__slots__ = 'name', 'arguments'


	def __init__(self, name: str, arguments: List[Argument]) -> None:
		self.name = name
		self.arguments = arguments


	def __str__(self) -> str:
		return f'<Instruction {self.name} with arguments {self.arguments}>'


	def __repr__(self) -> str:
		return self.__str__()
