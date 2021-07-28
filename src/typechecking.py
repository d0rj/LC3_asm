from typing import List, Tuple

from .asm_code.argument import Argument


def _type_missmatch_message(instr: str, types: List[str]) -> str:
    return f"'{instr.upper()}' instruction arguments must have types {types}."


def _count_missmatch_message(instr: str, required: int, passed: int) -> str:
    return "'%s' instruction must have %i arguments, but %i was gived." %\
        (instr.upper(), required, passed)


def arguments_matched(
        args: List[Argument], types: List[str], instr: str
        ) -> Tuple[bool, str]:
    """
    Returns flag that arguments matched the types pattern

    Args:
        args (List[Argument]): Actual arguments to check
        types (List[str]): Types pattern to ckeck
        instr (str): Instruction name. Required for error message

    Returns:
        Tuple[bool, str]: First element - flag that shows matching result
        (True if types are the same as in `types` pattern argument).
        Second element - error message. It will be empty if first element
        is True

    Examples:
        >>> args = [Argument('number', 1), Argument('number', 2)]
        >>> types = ['number', 'number']
        >>> arguments_matched(args, types, 'example')
        (True, '')

        >>> args = [Argument('number', 1)]
        >>> types = ['string']
        >>> arguments_matched(args, types, 'example2')
        (False, "'EXAMPLE2' instruction arguments must have types ['string'].")
    """
    if len(args) != len(types):
        return False, _count_missmatch_message(instr, len(types), len(args))

    all_matched = all(arg.type_ == type for arg, type in zip(args, types))

    if not all_matched:
        return False, _type_missmatch_message(instr, types)

    return True, str()


def arguments_matched_any(
        args: List[Argument], list_types: List[List[str]], instr: str
        ) -> Tuple[int, str]:
    """
    Returns flag that arguments matched any of types pattern in given list
    of patterns

    Args:
        args (List[Argument]): Actual arguments to check
        list_types (List[List[str]]): List of types patterns to check
        instr (str): Instruction name. Required for error message

    Returns:
        Tuple[int, str]: First element - index of matched types pattern in
        patterns list (-1 if no matched pattern). Second element - error
        message. It will be empty if first element is not equal -1. It will
        contain message for last pattern check

    Examples:
        >>> args = [Argument('number', 1), Argument('string', 'str')]
        >>> patterns = [['number', 'number'], ['number', 'string'], ['string']]
        >>> arguments_matched_any(args, patterns, 'example')
        (1, '')

        >>> args = [Argument('number', 1), Argument('string', 'str')]
        >>> patterns = [['string', 'number'], ['string']]
        >>> arguments_matched_any(args, patterns, 'example2')
        (-1, "'EXAMPLE2' instruction must have 1 arguments, but 2 was gived.")
    """
    for i, types in enumerate(list_types):
        matched, message = arguments_matched(args, types, instr)
        if matched:
            return i, str()

    return -1, message


def required_argument_types(args: List[Argument], types: List[str], instr: str):
    matched, message = arguments_matched(args, types, instr)
    if not matched:
        raise SyntaxError(message)
