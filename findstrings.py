import argparse, os, sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Find text strings in a binary file. Note: addresses are "
        "hexadecimal.",
        epilog="Table file: specifies how to convert bytes into printable "
        "characters; UTF-8; each line: byte (hexadecimal integer), space, "
        "character or hexadecimal Unicode codepoint (2 digits or more); empty "
        "lines, lines starting with '#' and trailing whitespace are ignored."
    )

    parser.add_argument(
        "-l", "--minimum-length", type=int, default=8,
        help="Minimum length of strings to find. Default=8."
    )
    parser.add_argument(
        "-r", "--maximum-repeat", type=int, default=8,
        help="Maximum repeat count of a byte. Default=8."
    )
    parser.add_argument(
        "-t", "--table-file",
        help="'Table file' to read (see below). Default=none "
        "(printable ASCII, i.e., bytes 0x20-0x7e)."
    )
    parser.add_argument(
        "input_file", help="Binary file to read and find strings in."
    )

    args = parser.parse_args()

    if args.minimum_length < 1:
        sys.exit("Invalid minimum string length.")
    if args.maximum_repeat < 1:
        sys.exit("Invalid maximum byte repeat count.")
    if args.table_file is not None and not os.path.isfile(args.table_file):
        sys.exit("Table file not found.")
    if not os.path.isfile(args.input_file):
        sys.exit("Input file not found.")

    return args

def read_table_file(handle):
    # read table file; generate non-empty non-comment lines without trailing
    # whitespace

    handle.seek(0)
    yield from(
        l.rstrip() for l in handle if l.rstrip() and not l.startswith("#")
    )

def parse_hexadecimal_integer(value, maxValue):
    # parse a hexadecimal integer from the table file

    try:
        value = int(value, 16)
        if not 0 <= value <= maxValue:
            raise ValueError
    except ValueError:
        sys.exit("Invalid hexadecimal integer in table file.")
    return value

def parse_table_file(handle):
    # parse a table file; yield one (int byte, str character) per call

    for line in read_table_file(handle):
        parts = line.split(" ")
        if len(parts) != 2:
            sys.exit("Syntax error in table file.")

        (byte, char) = parts
        byte = parse_hexadecimal_integer(byte, 0xff)
        if len(char) > 1:
            char = chr(parse_hexadecimal_integer(char, 0x10_ffff))
        yield (byte, char)

def read_file(handle):
    # generate file in chunks

    bytesLeft = handle.seek(0, 2)
    handle.seek(0)
    while bytesLeft:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def find_strings(handle, stringBytes, maxRepCnt):
    # read a binary file in chunks and find text strings (of any length)
    # stringBytes: set of bytes (integers) we're interested in
    # maxRepCnt: the maximum number a byte is allowed to repeat
    # generate: (position, bytes)

    # absolute position of chunk in file
    chunkPos = 0
    # current string of interesting bytes (may span multiple chunks)
    byteStr = bytearray()
    # absolute start position of byteStr in file
    startPos = None
    # how many times the last byte in byteStr has repeated
    repCnt = 0

    for chunk in read_file(handle):
        for (offset, byte) in enumerate(chunk):
            if byteStr and byte in stringBytes:
                # string byte inside string
                if byte != byteStr[-1]:
                    # string continues without repeat
                    byteStr.append(byte)
                    repCnt = 1
                elif repCnt < maxRepCnt:
                    # string continues with repeat
                    byteStr.append(byte)
                    repCnt += 1
                else:
                    # end string and start new one
                    yield (startPos, byteStr)
                    byteStr.clear()
                    byteStr.append(byte)
                    startPos = chunkPos + offset
                    repCnt = 1
            elif byteStr:
                # non-string byte ends string
                yield (startPos, byteStr)
                byteStr.clear()
            elif byte in stringBytes:
                # string byte starts string
                byteStr.append(byte)
                startPos = chunkPos + offset
                repCnt = 1
        # remember absolute position in file
        chunkPos += len(chunk)
    if byteStr:
        # end last string in file
        yield (startPos, byteStr)

def main():
    args = parse_arguments()

    if args.table_file is None:
        table = dict((i, chr(i)) for i in range(0x20, 0x7e + 1))
    else:
        # read table file
        try:
            with open(args.table_file, "rt", encoding="utf8") as handle:
                table = dict(parse_table_file(handle))
        except OSError:
            sys.exit("Error reading table file.")

    # find strings in input file
    try:
        with open(args.input_file, "rb") as handle:
            for (pos, bytes_) in find_strings(
                handle, set(table), args.maximum_repeat
            ):
                if len(bytes_) >= args.minimum_length:
                    print('{:04x}-{:04x}: «{:s}»'.format(
                        pos,
                        pos + len(bytes_) - 1,
                        "".join(table[byte] for byte in bytes_)
                    ))
    except OSError:
        sys.exit("Error reading input file.")

main()
