import argparse, os, re, sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Find text strings in a binary file and print them."
    )

    parser.add_argument(
        "-l", "--minimum-length", type=int, default=8,
        help="Only print strings with at least this many bytes. 1 or greater, "
        "default=8."
    )
    parser.add_argument(
        "-d", "--minimum-distinct", type=int, default=4,
        help="Only print strings with at least this many distinct bytes. 1 or "
        "greater, default=4."
    )
    parser.add_argument(
        "-r", "--maximum-repeat", type=int, default=8,
        help="If the same byte repeats this many times, end the string (and "
        "possibly print it, based on -l & -d), then start a new string. 1 or "
        "greater, default=8."
    )
    parser.add_argument(
        "-t", "--table-file",
        help="'Table file' to read (see README.md). Default=none."
    )
    parser.add_argument(
        "-c", "--csv", action="store_true",
        help="Output in CSV format (see README.md)."
    )
    parser.add_argument(
        "input_file", help="Binary file to read and find strings in."
    )

    args = parser.parse_args()

    if args.minimum_length < 1:
        sys.exit("Invalid minimum string length in arguments.")
    if args.minimum_distinct < 1:
        sys.exit("Invalid minimum number of distinct bytes in arguments.")
    if args.maximum_repeat < 1:
        sys.exit("Invalid maximum number of repeating bytes in arguments.")
    if args.table_file is not None and not os.path.isfile(args.table_file):
        sys.exit("Table file not found.")
    if not os.path.isfile(args.input_file):
        sys.exit("Input file not found.")

    return args

def read_table_file(handle):
    # generate lines from file (see comments for details)

    handle.seek(0)
    for line in handle:
        # ignore byte order mark (BOM)
        line = line.lstrip("\ufeff")
        # ignore leading and trailing whitespace
        line = line.strip()
        # convert strings of whitespace into a single space
        line = re.sub(r"\s+", " ", line)
        # ignore empty lines and comments
        if line and not line.startswith("#"):
            yield line

def parse_hexadecimal_integer(stri, maxValue):
    # parse a hexadecimal integer from the table file

    try:
        value = int(stri, 16)
    except ValueError:
        sys.exit("Invalid hexadecimal integer in table file: " + stri)

    if not 0 <= value <= maxValue:
        sys.exit("Hexadecimal integer out of range in table file: " + stri)
    return value

def parse_table_file(handle):
    # parse a table file; yield one (int byte, str character) per call

    for line in read_table_file(handle):
        parts = line.split(" ")
        if len(parts) != 2:
            sys.exit("Syntax error in table file: " + line)

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
        except UnicodeDecodeError:
            sys.exit("The table file is not a valid UTF-8 text file.")
        except OSError:
            sys.exit("Error reading table file.")

    if args.csv and '"' in table.values():
        print(
            "Warning: in CSV output mode, a table file without the character "
            "\" should be used, or the result might be unparseable."
        )

    # find strings in input file
    try:
        with open(args.input_file, "rb") as handle:
            for (pos, bytes_) in find_strings(
                handle, set(table), args.maximum_repeat
            ):
                if len(bytes_) >= args.minimum_length \
                and len(set(bytes_)) >= args.minimum_distinct:
                    decoded = "".join(table[byte] for byte in bytes_)
                    if args.csv:
                        print(f'{pos},{len(bytes_)},"{decoded}"')
                    else:
                        end = pos + len(bytes_) - 1
                        print(f'0x{pos:04x}-0x{end:04x}: «{decoded:s}»')
    except OSError:
        sys.exit("Error reading input file.")

main()
