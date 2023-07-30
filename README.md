# findstrings
```
usage: findstrings.py [-h] [-l MINIMUM_LENGTH] [-r MAXIMUM_REPEAT]
                      [-t TABLE_FILE]
                      input_file

Find text strings in a binary file and print them.

positional arguments:
  input_file            Binary file to read and find strings in.

options:
  -h, --help            show this help message and exit
  -l MINIMUM_LENGTH, --minimum-length MINIMUM_LENGTH
                        Minimum length of strings to find. Default=8.
  -r MAXIMUM_REPEAT, --maximum-repeat MAXIMUM_REPEAT
                        Maximum repeat count of a byte. Default=8.
  -t TABLE_FILE, --table-file TABLE_FILE
                        'Table file' to read (see README.md). Default=none.
```

## Table files
A *table file* is a UTF-8 text file specifies how to convert bytes in the
binary file into printable characters.

Each line consists of:
* a byte (hexadecimal integer between `00` and `ff`)
* a space
* one of these:
  * a single character (e.g. `å`)
  * a hexadecimal Unicode codepoint between `00` and `10ffff` (single-digit
codepoints must have a leading zero).

These are ignored:
* byte order mark (U+FEFF) at the start of the file
* trailing whitespace
* comment lines (lines starting with `#`)
* empty lines.

An example of a table file:
```
# this is a comment
# byte 0xf0 (240) becomes space (U+0020; trailing whitespace would be ignored)
f0 0020

# byte 0xf1 (241) becomes "å"
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
$ python3 findstrings.py -t tables/nes-smb1.txt -l 9 -r 2 smb1.nes
0x076c-0x0778: «BWORLD  TIMEW»
0x0796-0x07a0: «WORLD  - YC»
0x07c6-0x07ce: «GAME OVER»
(snip)
```
