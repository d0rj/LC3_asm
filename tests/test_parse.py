import pytest
from typing import List
from glob import glob

from lark.exceptions import UnexpectedCharacters, UnexpectedInput,\
    UnexpectedToken, UnexpectedEOF

from lc3asm.parsing import parse


def _get_examples_paths() -> List[str]:
    return glob('./examples/*.asm')


def test_parse_examples_passing():
    examples_paths = _get_examples_paths()
    
    assert len(examples_paths) > 0

    for example_path in examples_paths:
        try:
            with open(example_path, 'r') as file:
                programm = file.read()
            _ = parse(programm)
        except (UnexpectedCharacters, UnexpectedInput,
                UnexpectedToken, UnexpectedEOF):
            pytest.fail(f'Can\'t parse example \'{example_path}\'.')
