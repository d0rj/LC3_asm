from enum import Enum


MEMORY_SIZE = 65535


class NumberType:
    """
    Possible types of number representation in assembly code.

    Essentially, it's enum class in which every possible case has
    own string representation.

    Note:
        There are possible values: `HEX_NUMBER`, `BIN_NUMBER` and
        `DEC_NUMBER`.

        All values in lower-case.
    """

    HEX_NUMBER = 'hex_number'
    BIN_NUMBER = 'bin_number'
    DEC_NUMBER = 'dec_number'


class TokenType:
    """
    Possible token types for assembly code.

    Defined by rules for parser.

    Essentially, it's enum class in which every possible case has
    own string representation.

    Note:
        All values in lower-case.
    """

    NUMBER = 'number'
    LABEL = 'label'
    INSTRUCTION = 'instruction'
    PSEUDO_OP = 'pseudo_op'
    REGISTER_NAME = 'register_name'
    STRING = 'string'


class PseudoOperation:
    """
    List of assembler pseudo-operations' names.

    Defined by LC3 specification.

    Essentially, it's enum class in which every possible case has
    own string representation.

    Note:
        All values in lower-case.

        There are only supported pseudo-operations.
    """

    ORIG = '.orig'
    FILL = '.fill'
    STRINGZ = '.stringz'


class DictEnum(Enum):
    """
    Modified standart `enum.Enum`,
    in which you can access enum elements value by it's string name.

    Your enum need to inherit this class,
    if you wand to access enum elements by string.

    Note:
        To access elements value by string name
        you need to create class object,
        and then get enum element by square brackets.

        You can access only elements in full uppercase.

        Only overrides standart method `__getitem__`.

    Example:
        >>> class Test(DictEnum):
        >>>     A, B, C, D = range(4)
        >>> test = Test(0)
        >>> Test.C
        <Test.C: 2>
        >>> test['C']
        2
    """

    def __getitem__(self, key: str):
        """
        Square brackets access for enum's elements value by string.

        You can access only full uppercased enum elements.

        Args:
            key (str): Name of enum element. May be in any case.

        Returns:
            (any): Value of enum element.
        """
        return getattr(self.__class__, key.upper()).value


class Operations(DictEnum):
    """
    List of all supported LC3 assembly instructions and their
    bynary codes (`int` values).

    You can access instruction bincode by square brackets and string
    name of instruction, see `DictEnum`.

    Note:
        Most of commands has only their 4-bit command prefix as value.

        All `TRAP` subinstructions, for example `GETC` or `HALT`,
        has their full 2-byte representation.

        All `BR`(i.e. branch) subinstructions, for example `BRN` or `BRZP`,
        has their part representation (left 7 bits of 2-byte command).
    """

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
    """
    List of all LC3 registers and their numbers (offsets).

    You can access register offset by square brackets and string
    name of register, see `DictEnum`.
    """

    R0, R1, R2, R3, R4, R5, R6, R7, \
        PC, COND = range(10)
