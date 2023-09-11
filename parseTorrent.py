#!/usr/bin/python3
"""
Parse Contents of torrent file

TODO & Notes
    - Accept filename via command line

References:
    http://www.bittorrent.org/beps/bep_0003.html
    https://fileformats.fandom.com/wiki/Torrent_file
"""

import sys
import os


class TorrentFile:
    """Class representing parsed .torrent file metadata
    """
    def __init__(self, filename):
        self.filename = filename
        self.index = 1
        self.all_metadata = {} # Overarching dictionary structure
        self.fbytes = b''
        self.parse()

    def __getitem__(self, key):
        return self.all_metadata[key]

    def keys(self):
        return self.all_metadata.keys()

    def values(self):
        return self.all_metadata.values()

    @staticmethod
    def dictString(dictionary, indent_size=0):
        """Returns given dictionary in 'cleaner' string format
        """
        indent = '  ' * indent_size
        dstring = f"\n{indent}{{\n"

        for key, value in dictionary.items():
            if type(value) is dict:
                value = TorrentFile.dictString(value, indent_size+1)
            dstring += f"{indent}{key} : {value}\n"

        dstring += f"{indent}}}"
        return dstring

    def __str__(self):
        return f"File: {self.filename}\n" + self.dictString(self.all_metadata).strip() # Removes leading/trailing newlines

    def __parseByteString(self):
        """Parse bencoded bytes, either raw or utf-8

        Format: <length>:<contents>
        """
        ascii_len = ""
        count = 0
        for byte in self.fbytes[self.index:]:
            count += 1
            if chr(byte) == ':':
                break
            else:
                ascii_len += chr(byte)

        start_index = self.index + count
        self.index = start_index + int(ascii_len)
        try:
            bstring = self.fbytes[start_index:self.index].decode("utf-8")
        except UnicodeDecodeError:
            bstring = bytes(self.fbytes[start_index:self.index]).hex()

        return bstring

    def __parseInt(self):
        """Parse bencoded integer

        Format: i<base 10 ascii number>e
        """
        self.index += 1
        int_string = ""
        count = 0
        for byte in self.fbytes[self.index:]:
            count += 1
            if chr(byte) == 'e':
                break
            else:
                int_string += chr(byte)

        self.index += count
        return int(int_string)

    def __parseList(self):
        """Parse bencoded list

        Format: l<contents>e
        """
        self.index += 1
        itemlist = []

        while True:
            item = self.__parseNext()            
            if item == "END":
                break
            itemlist.append(item)

        self.index += 1
        return itemlist

    def __parseDictionary(self):
        """Parse bencoded dictionary

        Format: d<contents>e
        """
        self.index += 1
        meta_dict = {}

        while True:
            key = self.__parseNext()
            if key == "END":
                break
            meta_dict[key] = self.__parseNext()

        self.index += 1

        return meta_dict

    def __parseNext(self):
        """Used for parsing everything within overarching dictionary
        (Including other dictionaries)
        """
        infotype = chr(self.fbytes[self.index])
        if infotype == 'd':
            return self.__parseDictionary()
        elif infotype == 'e':
            return "END"
        elif infotype == 'i':
            return self.__parseInt()
        elif infotype == 'l':
            return self.__parseList()
        else:
            return self.__parseByteString()  


    def parse(self):
        """Parses out overarching dictionary

        This function assumes that the torrent file begins with 'd'
        """
        if self.fbytes == b'':
            with open(self.filename, "rb") as file:
                self.fbytes = file.read()
        while True:
            key = self.__parseNext()
            if key == "END":
                break
            self.all_metadata[key] = self.__parseNext()


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} FILENAME")
        return

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f"Unable to locate file '{filename}'")
        return

    tfile = TorrentFile(filename)
    print(tfile)



if __name__ == "__main__":
    sys.exit(main())
