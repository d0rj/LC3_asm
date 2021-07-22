from enum import Enum


MEMORY_SIZE = 65535


class NumberType:
    HEX_NUMBER = 'hex_number'
    BIN_NUMBER = 'bin_number'
    DEC_NUMBER = 'dec_number'


class TokenType:
    NUMBER = 'number'
    LABEL = 'label'
    INSTRUCTION = 'instruction'
    PSEUDO_OP = 'pseudo_op'
    REGISTER_NAME = 'register_name'
    STRING = 'string'


class PseudoOperation:
    ORIG = '.orig'
    FILL = '.fill'
    STRINGZ = '.stringz'


class DictEnum(Enum):
    def __getitem__(self, key: str):
        return getattr(self.__class__, key.upper()).value


class Operations(DictEnum):
    BR, ADD, LD, ST, \
    JSR, AND, LDR, STR, \
    RTI, NOT, LDI, STI, \
    JMP, RES, LEA, TRAP = range(16)

    GETC = 0xf0 << 8 | 0x20
    OUT = 0xf0 << 8 | 0x21
    PUTS = 0xf0 << 8 | 0x22
    IN = 0xf0 << 8 | 0x23
    PUTSP = 0xf0 << 8 | 0x24
    HALT = 0xf0 << 8 | 0x25

    BRN = 0b0000_100
    BRZ = 0b0000_010
    BRP = 0b0000_001
    BRNZ = BRN | BRZ
    BRNP = BRN | BRP
    BRZP = BRZ | BRP
    BRZNP = BRN | BRZ | BRP


class Registers(DictEnum):
    R0, R1, R2, R3, R4, R5, R6, R7, \
        PC, COND = range(10)
