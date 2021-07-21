from lark import Tree

from typing import List

from .lc3_constants import NumberType


def extract_label_name(tree: Tree) -> str:
	return str(tree.children[0])


def get_arguments_tree(tree: Tree) -> List[Tree]:
	args = [arg.children for arg in tree.children if isinstance(arg, Tree) and arg.data == 'arguments']
	args = args[0] if len(args) > 0 else []
	args = [arg.children[0] if arg.data == 'argument' else arg for arg in args]
	return args


def argument_type(tree: Tree) -> str:
	return tree.data


def instruction_name(tree: Tree) -> str:
	return str(tree.children[0]).lower()


def number_tree_to_int(tree: Tree) -> int:
	number_type = str(tree.children[0].type).lower()
	number_str = str(tree.children[0])

	if number_type == NumberType.HEX_NUMBER:
		return int(number_str, 16)
	if number_type == NumberType.BIN_NUMBER:
		return int(number_str, 2)
	if number_type == NumberType.DEC_NUMBER:
		return int(number_str)

	raise ValueError('Not a number.')
