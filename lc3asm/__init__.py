from typing import List

from lc3asm.parsing import parse as _parse
from lc3asm.assembling import process as _process


def process_source(source: str) -> List[int]:
    """
    One-line function to assemble source code and get memory stamp

    Essantially, it combines parsing from source string into AST and then
    assembling from AST to bytecode.

    Args:
        source (str): String with assembly source code

    Returns:
        List[int]: Memory for LC3 machine with 2-byte cells
    """
    parsed_tree = _parse(source)
    memory = _process(parsed_tree)
    return memory
