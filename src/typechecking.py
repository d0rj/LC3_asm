from typing import List, Tuple

from .asm_code.argument import Argument


def _argument_type_missmatch_message(instruction_name: str, required: str) -> str:
    return f'''\'{instruction_name.upper()}\' instruction arguments must have types {required}.'''


def _argument_count_missmatch_message(instruction_name: str, required: int, passed) -> str:
    return f'\'{instruction_name.upper()}\' instruction must have {required} arguments, but {passed} was gived.'


def arguments_matched(arguments: List[Argument], types: List[str], instr: str) -> Tuple[bool, str]:
    if len(arguments) != len(types):
        return False, _argument_count_missmatch_message(instr, len(types), arguments)

    all_matched = all(arg.type == _type for arg, _type in zip(arguments, types))

    if not all_matched:
        return False, _argument_type_missmatch_message(instr, str(types).replace('[', '').replace(']', ''))

    return True, str()


def arguments_matched_any(arguments: List[Argument], types: List[List[str]], instr: str) -> Tuple[int, str]:
    for i, _types in enumerate(types):
        matched, message = arguments_matched(arguments, _types, instr)
        if matched:
            return i, str()

    return -1, message


def required_argument_types(arguments: List[Argument], types: List[str], instr: str):
    matched, message = arguments_matched(arguments, types, instr)
    if not matched:
        raise SyntaxError(message)
