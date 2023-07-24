#!/usr/bin/python3
"""
Cyclical String Generator (for fuzzing)
"""
import sys
import argparse
import string

_NAME = "cyclic.py"
_VERSION = "v1.0.0"
_AUTHOR = "LCZ00"
_DESCRIPTION = f"""{_NAME} {_VERSION}, by {_AUTHOR}
CLI tool for creating cyclical strings, primarily for fuzzing purposes.
"""

class CyclicParser(argparse.ArgumentParser):
    """Override argparse class for better error handler"""
    def error(self, message="Unknown error", help=False):
        if help:
            self.print_help()
        else:
            print(f"Error, {message}")
            print(f"Try './{self.prog} --help' for more information.")
        sys.exit(1)


def parseArguments():
    parser = CyclicParser(
    prog=_NAME,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=_DESCRIPTION,
    epilog=f"Examples:\n\t{_NAME} 32\n\t{_NAME} -a ABC 8\n\t{_NAME} 64 --alphabet XY"
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'{_NAME} {_VERSION}',
        help='Show version number and exit'
    )
    parser.add_argument(
        '-a', '--alphabet',
        default=string.ascii_letters+string.digits,
        dest='alpha',
        help='Characters to use when generating output (Default: all ASCII letters/numbers)'
    )
    parser.add_argument(
        'length',
        type=int,
        help="Length of string to generate"
    )

    return parser.parse_args()


def cyclic(alphabet, length):
    alpha_len = len(alphabet)
    cyclic_str = ""

    for i in range(length):
        cyclic_str += alphabet[i % alpha_len]

    return cyclic_str


def main():
    args = parseArguments()
    print(cyclic(args.alpha, args.length))

if __name__ == "__main__":
    sys.exit(main())
