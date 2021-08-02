"""
Classes for assembler's inner AST representaion.

This assembler implementation for LC3 should operate with only list of
instructions to encode. Each instruction has their own list of argument.

For unified instruction representation assembler and other stuff uses
`Instriction` class from `instruction` submodule.

For unified argument representation assembler and other stuff uses
`Argument` class from `argument` submodule.

`Argument` class can be created directly from Lark's AST leaf
(and it's preffered way to create objects of that class). As a result,
this submodule depends on `src.utils` module.
"""
