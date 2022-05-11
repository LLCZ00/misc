#!/bin/python3

_NAME = "segmentCalculator.py"
_VERS = "1.0"
_AUTHOR = "LLCZ00"

"""
Calculates memory address from given segment

"""

import sys


def real_address(segment):
    try:
        seg = sys.argv[1].split(":", 1)
    except IndexError:
        error_handle("Addresses must be seperated with a colon: {}".format(segment))

    try:
        addrA = int(seg[0], 16)
        addrB = int(seg[1], 16)

    except ValueError:
        error_handle("Invalid hex number: {}".format(segment))

    real = (addrA * 16) + addrB

    print("Segment: {}:{}".format(hex(addrA), hex(addrB)))
    print("Real Address: {}".format(hex(real)))


def error_handle(msg):
    print("Error. {}\n".format(msg))
    sys.exit(
        "Usage: ./{} addressA:addressB\n(Numbers interpreted as hex, '0x' is optional)".format(
            _NAME
        )
    )


if __name__ == "__main__":

    if len(sys.argv) != 2:
        error_handle("1 argument required.")

    real_address(sys.argv[1])
