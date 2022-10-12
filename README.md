# findstrings
```
usage: findstrings.py [-h] [-l MINIMUM_LENGTH] [-r MAXIMUM_REPEAT]
                      [-t TABLE_FILE]
                      input_file

Find text strings in a binary file. Note: addresses are hexadecimal.

positional arguments:
  input_file            Binary file to read and find strings in.

options:
  -h, --help            show this help message and exit
  -l MINIMUM_LENGTH, --minimum-length MINIMUM_LENGTH
                        Minimum length of strings to find. Default=8.
  -r MAXIMUM_REPEAT, --maximum-repeat MAXIMUM_REPEAT
                        Maximum repeat count of a byte. Default=8.
  -t TABLE_FILE, --table-file TABLE_FILE
                        'Table file' to read (see below). Default=none
                        (printable ASCII, i.e., bytes 0x20-0x7e).

Table file: specifies how to convert bytes into printable characters; UTF-8;
each line: byte (hexadecimal integer), space, character or hexadecimal Unicode
codepoint (2 digits or more); empty lines, lines starting with '#' and
trailing whitespace are ignored.
```

## Examples
```
$ python3 findstrings.py doom2.exe
025c-0293: «DOS/4G  Copyright (C) Rational Systems, Inc. 1987 - 1993»
0c7c-0c85: «DOS16M.386»
0cb0-0cbf: «0123456789ABCDEF»
(snip)
```

```
$ python3 findstrings.py -t tables/nes-smb1.txt -l 9 -r 2 smb1.nes
076c-0778: «BWORLD  TIMEW»
0796-07a0: «WORLD  - YC»
07c6-07ce: «GAME OVER»
07d2-07e7: «LWELCOME TO WARP ZONE!»
(snip)
```
