from lark import Tree

from .tree_processing import argument_type, number_tree_to_int
from .lc3_constants import TokenType as TT


class Argument:
	__slots__ = 'type', 'value'


	def __init__(self, type: str, value) -> None:
		self.type = type
		self.value = value


	@classmethod
	def fromTree(cls, argument: Tree):
		arg_type = argument_type(argument)

		if arg_type == TT.NUMBER:
			return Argument(TT.NUMBER, number_tree_to_int(argument))
		if arg_type == TT.REGISTER_NAME:
			return Argument(TT.REGISTER_NAME, str(argument.children[0]))
		if arg_type == TT.LABEL:
			return Argument(TT.LABEL, str(argument.children[0]))
		if arg_type == TT.STRING:
			return Argument(TT.STRING, str(argument.children[0]))

		return None
