from typing import List

from .argument import Argument


class Instruction:
	__slots__ = 'name', 'arguments'


	def __init__(self, name: str, arguments: List[Argument]) -> None:
		self.name = name
		self.arguments = arguments
