from lark import Tree

from ..utils.tree_processing import argument_type, number_tree_to_int
from ..utils.lc3_constants import TokenType as TT


class Argument:
    __slots__ = 'type_', 'value'

    def __init__(self, type_: str, value) -> None:
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f'<Type: {self.type_}; Value: {self.value}>'

    def __repr__(self) -> str:
        return self.__str__()

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
