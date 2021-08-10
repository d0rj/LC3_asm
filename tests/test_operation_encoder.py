from random import randint
from typing import List

from lc3asm.ast.argument import Argument
from lc3asm.operation_encoder import OperationEncoder
from lc3asm.utils.constants import TokenType as TT


_operationEncoder = OperationEncoder()


def _random_case(string: str) -> str:
    return ''.join(
        c.upper() if randint(1, 10) % 2 == 0 else c.lower()
        for c in string
    )


def _encoded_must_be(op: str, args: List[Argument], right: int) -> None:
    op_names = [
        op.lower(),
        op.upper(),
        _random_case(op)]
    for op_name in op_names:
        assert _operationEncoder[op_name](args) == right


def test_encode_halt():
    _encoded_must_be('halt', [], 0xf025)


def test_encode_putsp():
    _encoded_must_be('putsp', [], 0xf024)


def test_encode_in():
    _encoded_must_be('in', [], 0xf023)


def test_encode_puts():
    _encoded_must_be('puts', [], 0xf022)


def test_encode_out():
    _encoded_must_be('out', [], 0xf021)


def test_encode_getc():
    _encoded_must_be('getc', [], 0xf020)


def test_encode_add():
    _encoded_must_be(
        'add',
        [
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.REGISTER_NAME, 'r2')
        ],
        0x16C2
    )
    _encoded_must_be(
        'add',
        [
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.REGISTER_NAME, 'r7'),
            Argument(TT.REGISTER_NAME, 'r2')
        ],
        0x17C2
    )

    _encoded_must_be(
        'add',
        [
            Argument(TT.REGISTER_NAME, 'r1'),
            Argument(TT.REGISTER_NAME, 'r1'),
            Argument(TT.NUMBER, -1)
        ],
        0x127F
    )
    _encoded_must_be(
        'add',
        [
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.REGISTER_NAME, 'r2'),
            Argument(TT.NUMBER, -14)
        ],
        0x16B2
    )
    _encoded_must_be(
        'add',
        [
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.REGISTER_NAME, 'r2'),
            Argument(TT.NUMBER, 7)
        ],
        0x16A7
    )


def test_encode_and():
    _encoded_must_be(
        'and',
        [
            Argument(TT.REGISTER_NAME, 'r1'),
            Argument(TT.REGISTER_NAME, 'r6'),
            Argument(TT.REGISTER_NAME, 'r4')
        ],
        0x5384
    )
    _encoded_must_be(
        'and',
        [
            Argument(TT.REGISTER_NAME, 'r0'),
            Argument(TT.REGISTER_NAME, 'r2'),
            Argument(TT.REGISTER_NAME, 'r1')
        ],
        0x5081
    )

    _encoded_must_be(
        'and',
        [
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.REGISTER_NAME, 'r3'),
            Argument(TT.NUMBER, 0)
        ],
        0x56E0
    )
    _encoded_must_be(
        'and',
        [
            Argument(TT.REGISTER_NAME, 'r0'),
            Argument(TT.REGISTER_NAME, 'r7'),
            Argument(TT.NUMBER, 4)
        ],
        0x51E4
    )


def test_encode_ld():
    _encoded_must_be(
        'ld',
        [
            Argument(TT.REGISTER_NAME, 'r1'),
            Argument(TT.NUMBER, 0x3008)
        ],
        0x2207
    )
    _encoded_must_be(
        'ld',
        [
            Argument(TT.REGISTER_NAME, 'r2'),
            Argument(TT.NUMBER, 0x3006)
        ],
        0x2405
    )


def _test_encode_br_with_delta(op: str, flag_delta: int):
    for offset in range(1, 0x1ff + 1):
        _encoded_must_be(
            op,
            [Argument(TT.NUMBER, offset)],
            offset + flag_delta
        )


def test_encode_br():
    _test_encode_br_with_delta('br', 0)


def test_encode_brn():
    _test_encode_br_with_delta('brn', 1 << 11)


def test_encode_brz():
    _test_encode_br_with_delta('brz', 1 << 10)


def test_encode_brp():
    _test_encode_br_with_delta('brp', 1 << 9)


def test_encode_brnz():
    _test_encode_br_with_delta('brnz', 0b110 << 9)


def test_encode_brnp():
    _test_encode_br_with_delta('brnp', 0b101 << 9)


def test_encode_brzp():
    _test_encode_br_with_delta('brzp', 0b011 << 9)


def test_encode_brnzp():
    _test_encode_br_with_delta('brnzp', 0b111 << 9)
