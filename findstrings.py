"""Find text strings in a binary file."""

import argparse
import os
import sys

def parse_arguments():
    """Parse command line arguments using argparse."""

    parser = argparse.ArgumentParser(
        description="Find text strings in a binary file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Table file: specifies how to convert bytes in input file into characters to print: "
        "UTF-8 text file; empty lines and lines starting with \"#\" are ignored; each line: byte "
        "(hexadecimal integer), space, character or hexadecimal Unicode codepoint (two digits or "
        "more)."
    )

    parser.add_argument(
        "-l", "--minimum-length", type=int, default=8, help="Minimum length of strings to find."
    )
    parser.add_argument(
        "-r", "--maximum-repeat", type=int, default=8, help="Maximum repeat count of a byte."
    )
    parser.add_argument(
        "-t", "--table-file", default="tables/ascii.txt", help="\"Table file\" to use (see below)."
    )
    parser.add_argument(
        "input_file", help="Binary file to find strings from."
    )

    args = parser.parse_args()

    if args.minimum_length < 1:
        sys.exit("Invalid minimum string length.")
    if args.maximum_repeat < 1:
        sys.exit("Invalid maximum byte repeat count.")
    if not os.path.isfile(args.table_file):
        sys.exit("Table file not found.")
    if not os.path.isfile(args.input_file):
        sys.exit("Input file not found.")

    return args

def read_table_file_lines(handle):
    """Read a table file. Generate non-empty non-comment lines without trailing newlines."""

    handle.seek(0)
    for line in handle:
        line = line[:-1] if line.endswith("\n") else line
        if line and not line.startswith("#"):
            yield line

def parse_hexadecimal_integer(value, maxValue):
    """Parse a hexadecimal integer from the table file."""

    try:
        value = int(value, 16)
        if not 0 <= value <= maxValue:
            raise ValueError
    except ValueError:
        sys.exit("Table file: invalid hexadecimal integer.")
    return value

def parse_table_file(handle):
    """Parse a table file. Yield one (int byte, str character) tuple per call."""

    for line in read_table_file_lines(handle):
        parts = line.split(" ")
        if len(parts) != 2:
            sys.exit("Table file: invalid number of space-separated parts on a line.")
        (byte, char) = parts

        byte = parse_hexadecimal_integer(byte, 0xff)
        if not char:
            sys.exit("Table file: no target character.")
        if len(char) > 1:
            char = chr(parse_hexadecimal_integer(char, 0x10ffff))

        yield (byte, char)

def read_file_in_chunks(handle):
    """Read file, yield one chunk per call."""

    bytesLeft = handle.seek(0, 2)
    handle.seek(0)
    while bytesLeft:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def find_strings(handle, stringBytes, maxRepCnt):
    """Read a binary file in chunks and find text strings (of any length).
    stringBytes: the set of bytes (integers) we're interested in
    maxRepCnt: the maximum number a byte is allowed to repeat
    yield: one (position, bytes) tuple per call"""

    chunkPos = 0  # absolute position of chunk in file
    byteStr = bytearray()  # current string of interesting bytes (may span multiple chunks)
    startPos = None  # absolute start position of byteStr in file
    repCnt = 0  # how many times the last byte in byteStr has repeated

    for chunk in read_file_in_chunks(handle):
        for (offset, byte) in enumerate(chunk):
            if byteStr and byte in stringBytes:
                # a string byte inside a string
                if byte != byteStr[-1]:
                    # a string continues without repeat
                    byteStr.append(byte)
                    repCnt = 1
                elif repCnt < maxRepCnt:
                    # a string continues with repeat
                    byteStr.append(byte)
                    repCnt += 1
                else:
                    # too many repeated bytes end a string and start a new one
                    yield (startPos, byteStr)
                    byteStr.clear()
                    byteStr.append(byte)
                    startPos = chunkPos + offset
                    repCnt = 1
            elif byteStr:
                # a non-string byte ends a string
                yield (startPos, byteStr)
                byteStr.clear()
            elif byte in stringBytes:
                # a string byte starts a string
                byteStr.append(byte)
                startPos = chunkPos + offset
                repCnt = 1
        # remember the absolute position in the file
        chunkPos += len(chunk)
    if byteStr:
        # end the last string in the file
        yield (startPos, byteStr)

def main():
    """The main function."""

    args = parse_arguments()

    # read the table file
    try:
        with open(args.table_file, "rt", encoding="utf8") as handle:
            table = dict(parse_table_file(handle))
    except OSError:
        sys.exit("Error reading the table file.")

    # find strings in the input file
    try:
        with open(args.input_file, "rb") as handle:
            for (pos, bytes_) in find_strings(handle, set(table), args.maximum_repeat):
                if len(bytes_) >= args.minimum_length:
                    print('0x{:04x}-0x{:04x}: "{:s}"'.format(
                        pos, pos + len(bytes_) - 1, "".join(table[byte] for byte in bytes_)
                    ))
    except OSError:
        sys.exit("Error reading the input file.")

if __name__ == "__main__":
    main()
