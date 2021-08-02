from dataclasses import dataclass
from typing import Any

from lark import Tree

from lc3asm.ast.adapting.from_lark import argument_type, number_tree_to_int
from lc3asm.utils.constants import TokenType as TT


@dataclass(frozen=True)
class Argument:
    """
    A class to represent an assembler instruction argument.

    Essentially, it's util class for two fields aggregation.

    Attributes:
        type_ (str): An argument type.
            Can be one of `utils.lc3_constants.TokenType`.
        value (any): Pythonic representation of argument.

    Methods:
        static `fromTree`.
    """

    __slots__ = 'type_', 'value'
    type_: str
    value: Any


    @classmethod
    def fromTree(cls, argument: Tree):
        """
        Static fabric from `lark.Tree` object.

        Args:
            argument (lark.Tree): Tree object with argument representation,
            builded from parser.

        Returns:
            (Argument | None): Returns constructed `Argument` object;
            or `None` if argument type not supported.

        Example:
            >>> str(example_tree)
            Tree('number', [Token('HEX_NUMBER', '0x3000')])
            >>> argument = Argument.fromTree(example_tree)
            >>> str(argument)
            <Type: number; Value: 12288>
        """
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
