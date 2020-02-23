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

def read_table_file_lines(handle):
    """Read a table file. Generate non-empty lines without trailing newlines."""

    handle.seek(0)
    for line in handle:
        line = line[:-1] if line.endswith("\n") else line
        if line:
            yield line

def parse_hexadecimal_integer(value, maxValue):
    """Parse a hexadecimal integer from the table file."""

    try:
        value = int(value, 16)
        if not 0 <= value <= maxValue:
            raise ValueError
    except ValueError:
        sys.exit("Table file: invalid hexadecimal value.")
    return value

def parse_table_file(handle):
    """Parse a table file. Yield one (int byte, str character) tuple per call."""

    for line in read_table_file_lines(handle):
        # split line by space
        parts = line.split(" ")
        if len(parts) != 2:
            sys.exit("Table file: invalid number of space-separated parts on a line.")
        (byte, char) = parts
        # parse byte
        byte = parse_hexadecimal_integer(byte, 0xff)
        # parse character/codepoint
        if not char:
            sys.exit("Table file: no target character.")
        if len(char) > 1:
            char = chr(parse_hexadecimal_integer(char, 0x10ffff))
        # yield byte&codepoint
        yield (byte, char)

def parse_arguments():
    """Parse command line arguments using getopt."""

    longOpts = ("minimum-length=", "maximum-repeat=", "table-file=")
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "l:r:t:", longOpts)
    except getopt.GetoptError:
        sys.exit("Invalid command line argument.")

    opts = dict(opts)

    # integer arguments
    minStrLen = parse_integer(opts.get("--minimum-length", opts.get("-l", "8")))
    maxRepCnt = parse_integer(opts.get("--maximum-repeat", opts.get("-r", "100")), 100)

    # table file (None = ASCII)
    tableFile = opts.get("--table-file", opts.get("-t"))
    if tableFile is None:
        table = dict(zip(range(0x20, 0x7f), (chr(cp) for cp in range(0x20, 0x7f))))
    else:
        if not os.path.isfile(tableFile):
            sys.exit("The table file does not exist.")
        try:
            with open(tableFile, "rt", encoding="utf8") as handle:
                table = dict((byte, codepoint) for (byte, codepoint) in parse_table_file(handle))
        except OSError:
            sys.exit("Error reading the table file.")

    # binary input file
    if len(args) != 1:
        sys.exit("Invalid number of command line arguments.")
    inputFile = args[0]
    if not os.path.isfile(inputFile):
        sys.exit("The input file does not exist.")

    return {
        "minStrLen": minStrLen,
        "maxRepCnt": maxRepCnt,
        "table": table,
        "inputFile": inputFile,
    }

def read_file_in_chunks(handle):
    """Read file, yield one chunk per call."""

    bytesLeft = handle.seek(0, 2)
    handle.seek(0)
    while bytesLeft:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def find_strings(handle, settings):
    """Read a binary file in chunks and find text strings. Yield one (position, bytes) tuple per
    call."""

    chunkPos = 0  # position of chunk in file
    string_ = bytearray()  # a string may span multiple chunks

    for chunk in read_file_in_chunks(handle):
        for (offset, byte) in enumerate(chunk):
            if not string_:
                if byte in settings["table"]:
                    # a string byte outside a string starts a new string
                    stringStartPos = chunkPos + offset
                    byteRepeatCnt = 1
                    string_.append(byte)
            else:
                if byte in settings["table"]:
                    if byte == string_[-1]:
                        if byteRepeatCnt == settings["maxRepCnt"]:
                            # too many repeated bytes in a string, so end it
                            if len(string_) >= settings["minStrLen"]:
                                yield (stringStartPos, string_)
                            string_.clear()
                        else:
                            # a string continues with a repeated byte (not too many yet)
                            byteRepeatCnt += 1
                            string_.append(byte)
                    else:
                        # a string continues with a non-repeated byte
                        byteRepeatCnt = 1
                        string_.append(byte)
                else:
                    # a non-string byte ends a string
                    if len(string_) >= settings["minStrLen"]:
                        yield (stringStartPos, string_)
                    string_.clear()
        # remember the absolute position in the file
        chunkPos += len(chunk)

    # end the last string in the file
    if len(string_) >= settings["minStrLen"]:
        yield (stringStartPos, string_)
    string_.clear()

def main():
    """The main function."""

    if sys.version_info[0] != 3:
        print("Warning: possibly incompatible Python version.", file=sys.stderr)

    settings = parse_arguments()

    try:
        with open(settings["inputFile"], "rb") as handle:
            for (startPos, string_) in find_strings(handle, settings):
                print("0x{:04x}: {:s}".format(
                    startPos, "".join(settings["table"][byte] for byte in string_)
                ))
    except OSError:
        sys.exit("Error reading the input file.")

if __name__ == "__main__":
    main()
