from typing import List
from dataclasses import dataclass

from lc3asm.asm_code.argument import Argument


@dataclass(frozen=True)
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
    name: str
    arguments: List[Argument]
