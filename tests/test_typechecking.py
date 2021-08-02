import pytest

from lc3asm.asm_code.argument import Argument
from lc3asm.typechecking import arguments_matched, arguments_matched_any,\
    required_argument_types,\
    _count_missmatch_message, _type_missmatch_message
from lc3asm.utils.constants import TokenType as TT


def test_arguments_matched_simple():
    for i in range(3):
        args = [Argument(TT.NUMBER, 10)] * i
        pattern = [TT.NUMBER] * i
        assert arguments_matched(args, pattern, 'count') == (True, str())

    args = [Argument(TT.NUMBER, 10), Argument(TT.STRING, 'strr')]
    pattern = [TT.NUMBER, TT.STRING]
    assert arguments_matched(args, pattern, 'different_types') == (True, str())

    args = [Argument('joke', 'ha'), Argument('math', 3.14)]
    pattern = ['joke', 'math']
    assert arguments_matched(args, pattern, 'unsupported') == (True, str())


def test_arguments_matched_unmatch():
    for i in range(3):
        args = [Argument(TT.NUMBER, 1)] * i
        pattern = [TT.NUMBER] * (i + 1)
        assert arguments_matched(args, pattern, 'count') ==\
            (False, _count_missmatch_message('count', len(pattern), len(args)))

    args = [Argument(TT.NUMBER, 10)]
    pattern = [TT.STRING]
    assert arguments_matched(args, pattern, 'types') ==\
        (False, _type_missmatch_message('types', pattern))

    args = [Argument(TT.NUMBER, 1), Argument(TT.STRING, 'test')]
    pattern = [TT.STRING, TT.NUMBER]
    assert arguments_matched(args, pattern, 'types_swap') ==\
        (False, _type_missmatch_message('types_swap', pattern))


def test_arguments_matched_any_simple():
    for i in range(3):
        args = [Argument(TT.NUMBER, 10)] * i
        pattern = [[TT.NUMBER] * i]
        assert arguments_matched_any(args, pattern, 'count') == (0, str())

    args = [Argument(TT.NUMBER, 10), Argument(TT.STRING, 'strr')]
    pattern = [[TT.NUMBER, TT.STRING]]
    assert arguments_matched_any(args, pattern, 'different_types') == (0, str())

    args = [Argument(TT.NUMBER, 10), Argument(TT.NUMBER, 20)]
    pattern = [
        [TT.STRING, TT.STRING],
        [TT.NUMBER, TT.NUMBER]
    ]
    assert arguments_matched_any(args, pattern, 'many') == (1, str())


def test_arguments_matched_any_unmatch():
    args = [Argument(TT.NUMBER, 10), Argument(TT.NUMBER, 20)]
    pattern = [
        [TT.NUMBER],
        [TT.NUMBER, TT.NUMBER, TT.NUMBER]
    ]
    assert arguments_matched_any(args, pattern, 'count') ==\
        (-1, _count_missmatch_message('count', len(pattern[1]), len(args)))

    args = [Argument(TT.NUMBER, 10), Argument(TT.NUMBER, 20)]
    pattern = [
        [TT.STRING, TT.STRING],
        [TT.STRING, TT.NUMBER]
    ]
    assert arguments_matched_any(args, pattern, 'many') ==\
        (-1, _type_missmatch_message('many', pattern[1]))


def test_required_argument():
    with pytest.raises(SyntaxError, match=r'.* must have .*'):
        for i in range(3):
            args = [Argument(TT.NUMBER, 1)] * i
            pattern = [TT.NUMBER] * (i + 1)
            required_argument_types(args, pattern, 'count')

    with pytest.raises(SyntaxError, match=r'.* must have .*'):
        args = [Argument(TT.NUMBER, 10)]
        pattern = [TT.STRING]
        required_argument_types(args, pattern, 'types')

    with pytest.raises(SyntaxError, match=r'.* must have .*'):
        args = [Argument(TT.NUMBER, 1), Argument(TT.STRING, 'test')]
        pattern = [TT.STRING, TT.NUMBER]
        required_argument_types(args, pattern, 'types_swap')

    try:
        for i in range(3):
            args = [Argument(TT.NUMBER, 10)] * i
            pattern = [TT.NUMBER] * i
            required_argument_types(args, pattern, 'count')
    except SyntaxError:
        pytest.fail('Same count raises exception.')

    try:
        args = [Argument(TT.NUMBER, 10), Argument(TT.STRING, 'strr')]
        pattern = [TT.NUMBER, TT.STRING]
        required_argument_types(args, pattern, 'different_types')
    except SyntaxError:
        pytest.fail('Same type raises exception.')
