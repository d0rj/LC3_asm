from lark import Lark

from src.assembler import assemble, preprocess, process


with open('./grammar/lc3_assembly.lark', 'r') as file:
	lc3_asm_grammar = file.read()

program = """
.orig 0x3000

ADD r0, 0xf125c, R0 
jmp 0b1001101
HALT

.someMetka: ; some comment
	jmp r5, 0x2
	HALT
add r0, r1, r5
jmp .someMetka
halt

.fill 0x5

.STRINGZ "Hello world"

.end
"""

l = Lark(lc3_asm_grammar)

process(l.parse(program))

# print(l.parse(program).pretty())
