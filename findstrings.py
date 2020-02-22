"""Find strings in binary files."""

import getopt
import os.path
import sys

def read_lines(file):
    """Read a UTF-8 text file. Yield one line without a newline per call."""

    with open(file, "rt", encoding="utf8") as handle:
        handle.seek(0)
        for line in handle:
            yield line[:-1] if line.endswith("\n") else line

def parse_table_file(file):
    """Parse a table file. Yield one (int byte, int codepoint) tuple per call."""

    for line in read_lines(file):
        # skip empty lines
        if line == "":
            continue
        # split line by space
        parts = line.split(" ")
        if len(parts) != 2:
            sys.exit("Invalid number of space-separated parts in table file.")
        (byte, char) = parts
        # parse byte
        try:
            byte = int(byte, 16)
            if not 0x00 <= byte <= 0xff:
                raise ValueError
        except ValueError:
            sys.exit("Invalid source byte value in table file.")
        # parse character
        if len(char) == 1:
            char = ord(char)
        else:
            try:
                char = int(char, 16)
                if not 0x0 <= char <= 0x10ffff:
                    raise ValueError
            except ValueError:
                sys.exit("Invalid target character/codepoint in table file.")
        # yield byte&character
        yield (byte, char)

def parse_arguments():
    """Parse command line options and arguments with getopt."""

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "m:t:", ("minimum-length=", "table-file="))
    except getopt.GetoptError:
        sys.exit("Invalid command line argument.")

    opts = dict(opts)

    # minimum length of strings
    minStrLen = opts.get("--minimum-length", opts.get("-m", "8"))
    try:
        minStrLen = int(minStrLen, 10)
        if minStrLen < 1:
            raise ValueError
    except ValueError:
        sys.exit("Invalid minimum length.")

    # table file (None = ASCII)
    tableFile = opts.get("--table-file", opts.get("-t"))
    if tableFile is None:
        table = dict(zip(range(0x20, 0x7f), range(0x20, 0x7f)))  # {0x20: 0x20, ..., 0x7e: 0x7e}
    else:
        if not os.path.isfile(tableFile):
            sys.exit("Table file does not exist.")
        table = dict((byte, codepoint) for (byte, codepoint) in parse_table_file(tableFile))

    # binary input file
    if len(args) != 1:
        sys.exit("Invalid number of command line arguments.")
    inputFile = args[0]
    if not os.path.isfile(inputFile):
        sys.exit("Input file does not exist.")

    return {
        "minStrLen": minStrLen,
        "table": table,
        "inputFile": inputFile,
    }

def convert_string(string_, table):
    """Convert bytes found in input file using the conversion table."""

    return "".join(chr(table[byte]) for byte in string_)

def find_strings(settings):
    """Find strings in binary file. Yield one (position, string) tuple per call."""

    # read file
    with open(settings["inputFile"], "rb") as handle:
        handle.seek(0)
        inputData = handle.read()

    startPos = None  # start position of current string
    for (pos, byte) in enumerate(inputData):
        isStringByte = byte in settings["table"]
        if startPos is None and isStringByte:
            # start a string
            startPos = pos
        elif startPos is not None and not isStringByte:
            # end a string
            if pos - startPos >= settings["minStrLen"]:
                yield (startPos, convert_string(inputData[startPos:pos], settings["table"]))
            startPos = None

    # end last string
    if startPos is not None and len(inputData) - startPos >= settings["minStrLen"]:
        yield (startPos, convert_string(inputData[startPos:], settings["table"]))

def main():
    """The main function."""

    if sys.version_info[0] != 3:
        print("Warning: possibly incompatible Python version.", file=sys.stderr)

    settings = parse_arguments()
    for (startPos, string_) in find_strings(settings):
        print(f"0x{startPos:04x}: {string_:s}")

if __name__ == "__main__":
    main()
