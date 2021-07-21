from lark import Tree

from typing import Dict

from .tree_processing import argument_type, number_tree_to_int
from .lc3_constants import TokenType as TT


def var_name(var: Dict[str, list]):
	return list(var.keys())[0]


def var_value(var: Dict[str, list]):
	return list(var.values())[0]


def var_from_tree(argument: Tree) -> Dict[str, list]:
	arg_type = argument_type(argument)

	if arg_type == TT.NUMBER:
		return { TT.NUMBER: number_tree_to_int(argument) }
	if arg_type == TT.REGISTER_NAME:
		return { TT.REGISTER_NAME: str(argument.children[0]) }
	if arg_type == TT.LABEL:
		return { TT.LABEL: str(argument.children[0]) }
	if arg_type == TT.STRING:
		return { TT.STRING: str(argument.children[0]) }

	return None
