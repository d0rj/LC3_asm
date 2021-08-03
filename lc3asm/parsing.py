from pathlib import Path

from lark import Lark, Tree


def _create_parser() -> Lark:
    base_path = Path(__file__).parent.resolve()
    with open(base_path / 'grammar/lc3_assembly.lark', 'r') as file:
        lc3_asm_grammar = file.read()
    return Lark(lc3_asm_grammar)


def parse(source: str) -> Tree:
    return _create_parser().parse(source)
