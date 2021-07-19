from lark import Lark

from src.assembler import process


with open('./grammar/lc3_assembly.lark', 'r') as file:
	lc3_asm_grammar = file.read()

program = """
.orig 0x3000

ADD r0, r5, R0 
jmp r2
HALT

.someMetka: ; some comment
	jmp r5
	HALT
add r0, r1, r5
jmp r2
halt

.fill 0x5

.STRINGZ "Hello world"

.end
"""

l = Lark(lc3_asm_grammar)

process(l.parse(program))

# print(l.parse(program).pretty())
