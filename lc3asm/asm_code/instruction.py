from typing import List

from lc3asm.asm_code.argument import Argument


class Instruction:
    """
    A class to represent an assembler instruction.

    Essentially, it's util class for two fields aggregation.

    Attributes:
        name (str): Name of assembly instruction.
        arguments (List[Argument]): List of arguments for this instruction.
        See `Argument` class.
    """

    __slots__ = 'name', 'arguments'

    def __init__(self, name: str, arguments: List[Argument]) -> None:
        """
        Assembly instruction constructor.

        Args:
            name (str): Name of assembly instruction.
            arguments (List[Argument]): List of arguments.
        """
        self.name = name
        self.arguments = arguments

    def __str__(self) -> str:
        """
        String representation of instruction.

        Returns:
            str: String representation in format
            <Instruction: ...; with arguments: ...>

        Example:
            >>> instr = Instruction('add', [Argument('number', 10)])
            >>> str(instr)
            <Instruction add with arguments [<Type: number; Value: 10>]>
        """
        return f'<Instruction {self.name} with arguments {self.arguments}>'

    def __repr__(self) -> str:
        """
        Simple `__repr__` override.

        Based on `__str__` private method and returns the same.
        """
        return self.__str__()
