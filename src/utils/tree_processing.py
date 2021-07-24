from lark import Tree

from typing import List

from .lc3_constants import NumberType


def label_name(tree: Tree) -> str:
    return str(tree.children[0])


def argument_type(tree: Tree) -> str:
    return tree.data


def instruction_name(tree: Tree) -> str:
    return str(tree.children[0]).lower()


def arguments_trees_of_tree(tree: Tree) -> List[Tree]:
    args: List[List[Tree]] = [
        arg.children
        for arg in tree.children
        if isinstance(arg, Tree) and arg.data == 'arguments'
        if isinstance(arg.children, list)
    ]
    args: List[Tree] = args[0] if len(args) > 0 else []
    args = [arg.children[0] if arg.data == 'argument' else arg for arg in args]
    return args


def extract_commands(root: Tree) -> List[Tree]:
    commands: List[Tree] = root.children
    # eat a 'command' ast node
    return [c.children[0] for c in commands]


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
