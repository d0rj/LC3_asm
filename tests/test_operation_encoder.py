from typing import List

from src.asm_code.argument import Argument
from src.operation_encoder import OperationEncoder
from src.utils.lc3_constants import TokenType as TT


_operationEncoder = OperationEncoder()


def _encoded_must_be(op: str, args: List[Argument], right: int) -> None:
    assert _operationEncoder[op](args) == right


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
