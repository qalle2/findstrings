# findstrings
Find text strings in a binary file.

## Syntax
```
usage: findstrings.py [-h] [-l MINIMUM_LENGTH] [-r MAXIMUM_REPEAT] [-t TABLE_FILE] input_file

Find text strings in a binary file.

positional arguments:
  input_file            Binary file to find strings from.

optional arguments:
  -h, --help            show this help message and exit
  -l MINIMUM_LENGTH, --minimum-length MINIMUM_LENGTH
                        Minimum length of strings to find. (default: 8)
  -r MAXIMUM_REPEAT, --maximum-repeat MAXIMUM_REPEAT
                        Maximum repeat count of a byte. (default: 8)
  -t TABLE_FILE, --table-file TABLE_FILE
                        "Table file" to use (see below). (default: tables/ascii.txt)

Table file: specifies how to convert bytes in input file into characters to print: UTF-8 text file; empty lines and
lines starting with "#" are ignored; each line: byte (hexadecimal integer), space, character or hexadecimal Unicode
codepoint (two digits or more).
```

## Examples
```
python findstrings.py doom2.exe
0x025c-0x0293: "DOS/4G  Copyright (C) Rational Systems, Inc. 1987 - 1993"
0x0c7c-0x0c85: "DOS16M.386"
(snip)
```

```
python findstrings.py --table-file tables\nes-smb1.txt --minimum-length 9 --maximum-repeat 2 smb1.nes
0x076c-0x0778: "BWORLD  TIMEW"
0x0795-0x07a0: "9WORLD  - YC"
0x07aa-0x07b9: "5MARIOYC7TIME UP"
0x07bd-0x07ce: "5MARIOYB9GAME OVER"
(snip)
```
