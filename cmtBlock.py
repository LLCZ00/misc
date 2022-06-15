#!/bin/python3

_NAME = "cmtBlock.py"
_VERS = "1.0"
_AUTHOR = "LLCZ00"

import sys


def help():
    print(
        """{0} {1}, by {2}

Description: Outputs the given string surrounded by the given/default character, 
for use as comments in whatever language accepts that character as a comment.
Default Character - #
Purly stylistic, based on my own preferences. 

Usage: ./{0} \"YOUR COMMENT\" [character]

Examples:
./{0} \"Surround with the default hash symbol\"
./{0} \"Surround with x's\" x
./{0} \"Surround with special symbol, stars\" \"*\"""".format(
            _NAME, _VERS, _AUTHOR
        )
    )
    sys.exit(0)


def make_comment_block(comment, char="#"):
    comment = "{} {} {}".format(char, comment, char)
    print("{0}\n{1}\n{0}".format(char * len(comment), comment))


def main():
    try:

        comment = sys.argv[1]
        if comment == "--help":
            help()

    except IndexError:
        print(
            "Error: Missing 'COMMENT'\nTry '{} --help' for more information.".format(
                _NAME
            )
        )
        sys.exit(1)

    try:
        char = sys.argv[2]
    except IndexError:
        make_comment_block(comment)  # Default
    else:
        make_comment_block(comment, char=char)  # Custom Character


if __name__ == "__main__":
    main()
