"""Find strings in binary files."""

import getopt
import os.path
import sys

def parse_integer(value, maxValue=None):
    """Parse a string containing an integer from command line."""

    try:
        value = int(value, 10)
        if value < 1 or maxValue is not None and value > maxValue:
            raise ValueError
    except ValueError:
        sys.exit("Arguments: invalid integer value.")
    return value

def parse_arguments():
    """Parse command line arguments using getopt."""

    longOpts = ("minimum-length=", "maximum-repeat=", "table-file=", "start-quote=", "end-quote=")
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "l:r:t:", longOpts)
    except getopt.GetoptError:
        sys.exit("Invalid command line argument.")

    opts = dict(opts)

    # integer arguments
    minStrLen = parse_integer(opts.get("--minimum-length", opts.get("-l", "8")))
    maxRepCnt = parse_integer(opts.get("--maximum-repeat", opts.get("-r", "100")), 100)

    # string arguments
    startQuote = opts.get("--start-quote", '"')
    endQuote = opts.get("--end-quote", '"')

    # table file
    tableFile = opts.get("--table-file", opts.get("-t", "tables/ascii.txt"))
    if not os.path.isfile(tableFile):
        sys.exit("The table file does not exist.")

    # input file
    if len(args) != 1:
        sys.exit("Invalid number of command line arguments.")
    inputFile = args[0]
    if not os.path.isfile(inputFile):
        sys.exit("The input file does not exist.")

    return {
        "minStrLen": minStrLen,
        "maxRepCnt": maxRepCnt,
        "tableFile": tableFile,
        "startQuote": startQuote,
        "endQuote": endQuote,
        "inputFile": inputFile,
    }

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

def create_output_format_string(settings):
    """Create a string to .format() the output with."""

    try:
        inputFileSize = os.path.getsize(settings["inputFile"])
    except OSError:
        sys.exit("Error getting input file size.")
    if inputFileSize == 0:
        sys.exit("The input file is empty.")
    maxHexPosLen = len(format(inputFileSize - 1, "x"))
    return "0x{{:0{:d}x}}: {:s}{{:s}}{:s}".format(
        maxHexPosLen, settings["startQuote"], settings["endQuote"]
    )

def main():
    """The main function."""

    if sys.version_info[0] != 3:
        print("Warning: possibly incompatible Python version.", file=sys.stderr)

    settings = parse_arguments()

    # read the table file
    try:
        with open(settings["tableFile"], "rt", encoding="utf8") as handle:
            table = dict(parse_table_file(handle))
    except OSError:
        sys.exit("Error reading the table file.")

    # find strings in the input file
    lineFormat = create_output_format_string(settings)
    try:
        with open(settings["inputFile"], "rb") as handle:
            for (startPos, bytes_) in find_strings(handle, frozenset(table), settings["maxRepCnt"]):
                if len(bytes_) >= settings["minStrLen"]:
                    print(lineFormat.format(startPos, "".join(table[byte] for byte in bytes_)))
    except OSError:
        sys.exit("Error reading the input file.")

if __name__ == "__main__":
    main()
