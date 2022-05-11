#!/usr/bin/python3.9
"""
Script for printing out hex of nasm-compiled ASM files
"""
import sys
from os import path


class ArgumentHandler:
    def __init__(self):
        self.filename = None
        self.flags = {"preamble": 1, "endian": sys.byteorder, "dup": 0, "offset": 0}

        self.argeParse()

    @staticmethod
    def usage():
        print(
            """Usage: hexPrint.py [options] FILENAME

Options:

-h, --help       Help (this page)
-p, --nopre      Turn off preamble
-a, --all        Print all lines
-o NUMBER        Set offset (default: 0)
"""
        )
        exit(0)

    @staticmethod
    def error(msg=None):
        if msg != None:
            print(msg)
        print(
            "Usage: hexPrint.py [options] FILENAME\ntry 'hexPrint.py --help' for more information"
        )
        sys.exit(-1)

    def argeParse(self):
        if len(sys.argv) == 1:
            self.error()

        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            self.usage()

        if not path.exists(sys.argv[-1]):
            self.error("No file found")
        self.filename = sys.argv.pop()

        args = iter(sys.argv[1:])
        while True:
            arg = next(args, "end")
            if arg == "end":
                break

            elif arg == "-p" or arg == "--nopre":
                self.flags["preamble"] = 0

            elif arg == "-a" or arg == "--all":
                self.flags["dup"] = 1

            elif arg == "-h" or arg == "--help":
                self.usage()

            elif arg == "-o":
                offset = next(args, "end")
                if not offset.isdigit():
                    self.error("Offset flag requires number")
                self.flags["offset"] = int(offset)

            elif arg == "-e":
                endin = next(args, "end")
                if endin != "big" and endin != "little":
                    self.error("Invalid endianness: {}".format(endin))
                self.flags["endian"] = endin

            else:
                self.error("Invalid argument: {}".format(arg))


class HexPrint(ArgumentHandler):
    def __init__(self):
        super().__init__()

        if self.flags["preamble"]:
            self.preamble()

        if self.flags["dup"]:
            self.printAll()
        else:
            self.noDuplicates()

    def preamble(self):
        print("File: {}".format(self.filename))
        print("Endianness: {}\n".format(sys.byteorder))

    def hexGen(self):
        with open(self.filename, "rb") as bin:
            bin.seek(self.flags["offset"])
            for line in iter(lambda: bin.read(16), b""):
                yield line, (bin.tell() - 16).to_bytes(4, byteorder="big")

    def printAll(self):
        for line, place in self.hexGen():
            print("{} {}".format(place.hex(), line.hex(" ", 2)))

    def noDuplicates(self):
        last_line = 0
        dup_flag = 0

        for line, place in self.hexGen():
            if line != last_line:
                print("{} {}".format(place.hex(), line.hex(" ", 2)))
                dup_flag = 0
                last_line = line

            elif dup_flag == 0:
                print("*")
                dup_flag = 1
                last_line = line


if __name__ == "__main__":
    HexPrint()
