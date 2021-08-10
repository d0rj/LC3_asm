from typing import Dict, List, Tuple

from lark import Tree

from lc3asm.operation_encoder import OperationEncoder
from lc3asm.typechecking import required_argument_types
from lc3asm.ast.argument import Argument
from lc3asm.ast.instruction import Instruction
from lc3asm.utils.constants import MEMORY_SIZE,\
    TokenType as TT, PseudoOperation as PO
from lc3asm.ast.adapting.from_lark import instruction_name, label_name,\
    arguments_trees_of_tree, extract_commands


def _arguments_from_tree(command: Tree) -> List[Argument]:
    return [
        Argument.fromTree(arg_tree)
        for arg_tree in arguments_trees_of_tree(command)
    ]


def preprocess(
        tree: Tree, memory: List[int]
        ) -> Tuple[Dict[int, Instruction], List[int]]:
    current_address = 0

    labels: Dict[str, int] = {}
    commands = extract_commands(tree)

    instructions: Dict[int, Tree] = {}

    for command in commands:
        if command.data == TT.INSTRUCTION:
            instructions[current_address] = command
        elif command.data == TT.LABEL:
            labels[label_name(command)] = current_address
            current_address -= 1
        elif command.data == TT.PSEUDO_OP:
            if instruction_name(command) == PO.ORIG:
                arguments = _arguments_from_tree(command)
                required_argument_types(arguments, [TT.NUMBER], PO.ORIG)
                current_address = int(arguments[0].value) - 1
            elif instruction_name(command) == PO.FILL:
                arguments = _arguments_from_tree(command)
                required_argument_types(arguments, [TT.NUMBER], PO.FILL)
                memory[current_address] = int(arguments[0].value)
            elif instruction_name(command) == PO.STRINGZ:
                arguments = _arguments_from_tree(command)
                required_argument_types(arguments, [TT.STRING], PO.STRINGZ)

                string = str(arguments[0].value).replace('"', '')
                _bytes = bytearray(bytes(string, 'ascii'))
                _bytes.append(0x00)
                memory[current_address:(current_address + len(_bytes))] = _bytes
                current_address += len(_bytes) - 1
        else:
            raise SyntaxError(f'Unknown command: {command.children[0]}.')

        current_address += 1

    result: Dict[int, Instruction] = {}
    for addr, instruction in instructions.items():
        name = instruction_name(instruction)
        arguments = _arguments_from_tree(instruction)
        # replace labels with address
        arguments = [
            Argument(TT.NUMBER, labels[arg.value])
            if arg.type_ == TT.LABEL
            else arg
            for arg in arguments
        ]
        result[addr] = Instruction(name, arguments)

    return result, memory


def assemble(
        instructions: Dict[int, Instruction], memory: List[int]
        ) -> List[int]:
    encode_operation = OperationEncoder()

    for addr, instr in instructions.items():
        encoded = encode_operation[instr.name](instr.arguments)
        memory[addr] = encoded

    return memory


def process(tree: Tree) -> List[int]:
    memory = [0 for _ in range(MEMORY_SIZE)]

    if tree.data != 'start':
        raise ValueError('Unsupported tree format passed to function.')

    instructions, memory = preprocess(tree, memory)
    memory = assemble(instructions, memory)

    return memory
