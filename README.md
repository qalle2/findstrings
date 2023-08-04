# findstrings
Find text strings in a binary file and print them.

Table of contents:
* [Command line help text](#command-line-help-text)
* [Output modes](#output-modes)
* [Table files](#table-files)
* [Examples](#examples)

## Command line help text
```
usage: findstrings.py [-h] [-l MINIMUM_LENGTH] [-d MINIMUM_DISTINCT]
                      [-r MAXIMUM_REPEAT] [-t TABLE_FILE] [-c]
                      input_file

Find text strings in a binary file and print them.

positional arguments:
  input_file            Binary file to read and find strings in.

options:
  -h, --help            show this help message and exit
  -l MINIMUM_LENGTH, --minimum-length MINIMUM_LENGTH
                        Only print strings with at least this many bytes. 1 or
                        greater, default=8.
  -d MINIMUM_DISTINCT, --minimum-distinct MINIMUM_DISTINCT
                        Only print strings with at least this many distinct
                        bytes. 1 or greater, default=4.
  -r MAXIMUM_REPEAT, --maximum-repeat MAXIMUM_REPEAT
                        If the same byte repeats this many times, end the
                        string (and possibly print it, based on -l & -d), then
                        start a new string. 1 or greater, default=8.
  -t TABLE_FILE, --table-file TABLE_FILE
                        'Table file' to read (see README.md). Default=none.
  -c, --csv             Output in CSV format (see README.md).
```

## Output modes
* Default (non-CSV) mode: For each string, print the start and end address in
hexadecimal and the string in `«»` quotes.
* CSV mode (machine-readable): For each string, print the start address and
length in decimal and the string in `""` quotes. The table file (see below)
should not contain the `"` character.

## Table files
A *table file* is a UTF-8 text file that specifies how to convert bytes in the
binary file into printable characters.

Each line consists of:
* byte value to convert from (hexadecimal integer between `00` and `ff`)
* one or more whitespace characters (space, tab, etc.)
* character to convert into, in one of these formats:
  * a single character (e.g. `å`)
  * a hexadecimal Unicode codepoint between `00` and `10ffff` (single-digit
codepoints must have a leading zero)

These are ignored:
* byte order mark (BOM, U+FEFF) at the start of the file (or any line, to be
precise)
* leading and trailing whitespace
* comment lines (lines starting with `#`)
* empty lines.

Note that whitespace characters must be written as codepoints, as otherwise
they'd be ignored as trailing whitespace. E.g. space can be written as `0020`
and ideographic space as `3000`.

An example of a table file:
```
# byte 0xf0 becomes a space
f0 0020
# byte 0xf1 becomes "å"
f1 å
```

If no table file is specified, bytes `0x20`&ndash;`0x7e` (printable ASCII) are
converted into their respective characters, and other bytes are ignored.

## Examples
```
$ python3 findstrings.py doom.exe
0x025c-0x0293: «DOS/4G  Copyright (C) Rational Systems, Inc. 1987 - 1993»
0x0c7c-0x0c85: «DOS16M.386»
0x0cb0-0x0cbf: «0123456789ABCDEF»
(snip)
```

```
$ python3 findstrings.py -c doom.exe
604,56,"DOS/4G  Copyright (C) Rational Systems, Inc. 1987 - 1993"
3196,10,"DOS16M.386"
3248,16,"0123456789ABCDEF"
(snip)
```

```
$ python3 findstrings.py -t tables/nes-smb1.txt -l 9 -r 2 smb1.nes
0x076c-0x0778: «BWORLD  TIMEW»
0x0796-0x07a0: «WORLD  - YC»
0x07c6-0x07ce: «GAME OVER»
(snip)
```
