from lark import Lark, Tree


def _create_parser() -> Lark:
    with open('./grammar/lc3_assembly.lark', 'r') as file:
        lc3_asm_grammar = file.read()
    return Lark(lc3_asm_grammar)


def parse(source: str) -> Tree:
    return _create_parser().parse(source)
