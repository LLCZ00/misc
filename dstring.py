"""
Converts string to little-endian, 4 byte chunks.
My reasons are my own.
"""

import sys

def dwordstring(string):
    bytestring = bytearray([ord(byte) for byte in string])
    bytestring.reverse()
    bytestring = [bytestring[i:i+4] for i in range(0, len(bytestring), 4)]
    for dword in bytestring:
        print(f"0x{''.join(f'{byte:x}' for byte in dword)}") 
    
def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} STRING")
        return 1
    dwordstring(sys.argv[1])
    
    
if __name__ == "__main__":
    sys.exit(main())
