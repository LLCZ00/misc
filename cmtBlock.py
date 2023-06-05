#!/bin/python3
#
# Copyright (C) 2023 LLCZ00
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
#

"""
Comment Block Generator
"""

import sys
import argparse

_NAME = "cmtblock.py"
_VERSION = "1.1.0"
_AUTHOR = "LLCZ00"
_DESCRIPTION = f"""{_NAME} {_VERSION}, by {_AUTHOR}
Script/tool for creating comment 'block' in desired language's style.
Basedd purely on my own preferences.
"""

class CMTParser(argparse.ArgumentParser):
    """Override argparse class for better error handler"""
    def error(self, message="Unknown error", help=False):
        if help:
            self.print_help()
        else:
            print(f"Error. {message}")
            print(f"Try './{self.prog} --help' for more information.")
        sys.exit(1)


def parseArguments():
    parser = CMTParser(
    prog=_NAME,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=_DESCRIPTION,
    epilog=f"Examples:\n\t{_NAME} comment\n\t{_NAME} --style c \"C-styled comment block\""
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'{_NAME} v{_VERSION}',
        help='Show version number and exit'
    )
    parser.add_argument(
        '--style', 
        choices=["python", "c"],
        dest='style',
        type=str.lower,
        default="python",
        help='Language style to return comment block in (Case insensitive).'
    )
    parser.add_argument(
        'comment',
        help="Comment to 'blockify'"
    )
    return parser.parse_args()


class Comment:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return str(self.content)

    def __style_python(self):
        cmt = f"# {self.content} #"
        bookend = '#' * len(cmt)
        return f"{bookend}\n{cmt}\n{bookend}"

    def __style_c(self):
        cmt = f"* {self.content} *"
        bookend_top = f"/*{'*' * (len(cmt) - 2)}"
        bookend_bottom = f"{'*' * (len(cmt) - 2)}*/"
        return f"{bookend_top}\n{cmt}\n{bookend_bottom}"

    def __format__(self, style="python"):
        if style == "python":
            return self.__style_python()
        elif style == "c":
            return self.__style_c()
        else:
            return self.content


def main():
    args = parseArguments()
    comment = Comment(args.comment)
    print(format(comment, args.style))


if __name__ == "__main__":
    sys.exit(main())
