from src.asm_code.argument import Argument
from src.typechecking import arguments_matched
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
