from src.asm_code.argument import Argument
from src.typechecking import arguments_matched,\
    _count_missmatch_message, _type_missmatch_message
from src.utils.lc3_constants import TokenType as TT


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
