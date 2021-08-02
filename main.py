import argparse
import os

from src.assembler import process
from src.parser import parse


def parse_cmd_arguments() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-p', '--path',
        help='Path to assembly source',
        type=str,
        default='./examples/hello_world.asm'
    )
    arg_parser.add_argument(
        '-o', '--out',
        help='Path of output file',
        type=str,
        default='./output_programms/hello_world.raw'
    )

    args = arg_parser.parse_args()
    if not args.path:
        raise AttributeError('Missed required parameter --path')
    if not args.out:
        raise AttributeError('Missed required parameter --out')

    if not os.path.exists(args.path):
        raise FileExistsError(f'File \'{args.path}\' does not exists')

    return args


def main() -> None:
    args = parse_cmd_arguments()

    with open(args.path, 'r') as file:
        program = file.read()

    parsed_tree = parse(program)
    memory = process(parsed_tree)
    byte_memory = bytearray([
        e
        for m in memory
        for e in (m & 0xff, (m & 0xff00) >> 8)
    ])

    with open(args.out, 'wb') as file:
        file.write(byte_memory)


if __name__ == '__main__':
    main()
