from lark import Tree

from ..utils.tree_processing import argument_type, number_tree_to_int
from ..utils.lc3_constants import TokenType as TT


class Argument:
    """
    A class to represent an assembler instruction  argument.

    Essentially, it's util class for two fields aggregation.

    Attributes:
        type_ (str): An argument type.
            Can be one of :class:`utils.lc3_constants.TokenType`.
        value (any): Pythonic representation of argument.

    Methods:
        static :meth:`fromTree`.
    """

    __slots__ = 'type_', 'value'

    def __init__(self, type_: str, value) -> None:
        """
        Instruction's argument constructor.

        Note:
            It is recommended not to use it directly,
            but to create objects of this class
            using a static method :meth:`Argument.fromTree`.

        Args:
            type_ (str): An argument type.
                Can be one of :class:`utils.lc3_constants.TokenType`.
            value (any): Pythonic representation of an argument.
        """
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        """
        String representation of argument.

        Returns:
            str: String representation in format <Type: ...; Value: ...>

        Example:
            >>> str(Argument('number', 42))
            <Type: number; Value: 42>
        """
        return f'<Type: {self.type_}; Value: {self.value}>'

    def __repr__(self) -> str:
        """
        Simple `__repr__` override.

        Based on :meth:`__str__` private method and returns the same.
        """
        return self.__str__()

    @classmethod
    def fromTree(cls, argument: Tree):
        """
        Static fabric from :class:`lark.Tree` object.

        Args:
            argument (lark.Tree): Tree object with argument representation,
            builded from parser.

        Returns:
            (Argument | None): Returns constructed :class:`Argument` object;
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
