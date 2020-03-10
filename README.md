# findstrings
Find text strings in a binary file.

## Syntax
```
usage: findstrings.py [-h] [-l MINSTRLEN] [-r MAXREPCNT] [-t TABLEFILE] [--start-quote STARTQUOTE]
                      [--end-quote ENDQUOTE]
                      inputFile

Find strings in a binary file.

positional arguments:
  inputFile             the binary file to find strings from

optional arguments:
  -h, --help            show this help message and exit
  -l MINSTRLEN, --minimum-length MINSTRLEN
                        minimum length of strings to find (minimum: 1, default: 8)
  -r MAXREPCNT, --maximum-repeat MAXREPCNT
                        maximum repeat count of a byte (minimum: 1, default/maximum: 100)
  -t TABLEFILE, --table-file TABLEFILE
                        the "table file" that describes how to convert bytes into characters (see below; default:
                        tables/ascii.txt)
  --start-quote STARTQUOTE
                        character(s) to be printed before each string (default: ")
  --end-quote ENDQUOTE  character(s) to be printed after each string (default: ")

Table files: UTF-8; empty lines and lines starting with "#" are ignored; each line: byte in input file (hexadecimal
integer 00-ff), space, what to print (a character or a hexadecimal Unicode codepoint with at least two digits, i.e.,
00-10ffff).
```

## Examples
```
python findstrings.py test\doom2.exe
0x0025c: "DOS/4G  Copyright (C) Rational Systems, Inc. 1987 - 1993"
0x00c7c: "DOS16M.386"
(snip)
```

```
python findstrings.py --table-file tables\nes-smb1.txt --minimum-length 9 --maximum-repeat 2 --start-quote "" --end-quote "" test\smb1.nes
0x076c: BWORLD  TIMEW
0x0795: 9WORLD  - YC
(snip)
```
