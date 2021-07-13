from lark import Lark


with open('./lc3_assembly.lark', 'r') as file:
	lc3_asm_grammar = file.read()

program = """
0x3000
ADD r0, 0xf125c, R0 
jmp 0b1001101
TRAP
"""

l = Lark(lc3_asm_grammar)

print(l.parse(program).pretty())
