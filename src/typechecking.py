from typing import List, Tuple

from .asm_code.argument import Argument


def _type_missmatch_message(instr: str, types: List[str]) -> str:
    return f"\'{instr.upper()}\' instruction arguments must have types {types}."


def _count_missmatch_message(instr: str, required: int, passed: int) -> str:
    return f'\'{instr.upper()}\' instruction must have {required} arguments, but {passed} was gived.'


def arguments_matched(
        args: List[Argument], types: List[str], instr: str
        ) -> Tuple[bool, str]:
    if len(args) != len(types):
        return False, _count_missmatch_message(instr, len(types), len(args))

    all_matched = all(arg.type_ == type for arg, type in zip(args, types))

    if not all_matched:
        return False, _type_missmatch_message(instr, types)

    return True, str()


def arguments_matched_any(
        args: List[Argument], list_types: List[List[str]], instr: str
        ) -> Tuple[int, str]:
    for i, types in enumerate(list_types):
        matched, message = arguments_matched(args, types, instr)
        if matched:
            return i, str()

    return -1, message


def required_argument_types(args: List[Argument], types: List[str], instr: str):
    matched, message = arguments_matched(args, types, instr)
    if not matched:
        raise SyntaxError(message)
