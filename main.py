from lark import Lark

from src.assembler import process


with open('./grammar/lc3_assembly.lark', 'r') as file:
    lc3_asm_grammar = file.read()

with open('./examples/hello_world.asm', 'r') as file:
    program = file.read()

lark = Lark(lc3_asm_grammar)

memory = process(lark.parse(program))
byte_memory = bytearray([e for m in memory for e in (m & 0xff, (m & 0xff00) >> 8)])

with open('./output_programms/hello_world.raw', 'wb') as file:
    file.write(byte_memory)
