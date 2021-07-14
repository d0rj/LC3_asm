from lark import Lark


with open('./lc3_assembly.lark', 'r') as file:
	lc3_asm_grammar = file.read()

program = """
.orig 0x3000

ADD r0, 0xf125c, R0 
jmp 0b1001101
HALT

.someMetka:
	jmp r5, 0x2
	HALT
add r0, r1, r5
jmp .someMetka
halt

.end
"""

l = Lark(lc3_asm_grammar)

print(l.parse(program).pretty())
