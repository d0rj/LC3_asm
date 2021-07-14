# LC3_asm

## Overview

⚠WIP - now it can only parse grammar⚠

Simple asssembler for LC3 virtual machine. You can see my own realization of VM [there](https://github.com/d0rj/LC3_vm).

### Supports

- [x] Instructions
- [x] All types of arguments for instruction
- [x] Labels
- [ ] Advanced label declaration
- [x] Meta assebler directives (like ***.STRINGZ***)
- [ ] Machine code generation
- [ ] AST optimization of assembly code

### Dependencies

[Lark package](https://github.com/lark-parser/lark) for easy and pretty [EBNF grammar](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) parsing and [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) generation.

## Resources

* [Some example of assembly language (Jupyter notebook)](https://jupyter.brynmawr.edu/services/public/dblank/CS240%20Computer%20Organization/2015-Fall/Notes/LC3%20Assembly%20Language.ipynb)

* [Doc file](http://people.cs.georgetown.edu/~squier/Teaching/HardwareFundamentals/LC3-trunk/docs/LC3-AssemblyManualAndExamples.pdf)
