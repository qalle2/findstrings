# findstrings
Find text strings in a binary file.

## Syntax
*options* *input_file*

### *options*
* `-m` *length*, `--minimum-length` *length*
  * minimum length of strings to find
  * minimum: 1, default: 8
* `-t` *file*, `--table-file` *file*
  * specifies a "table file" that contains rules for converting bytes in *input_file* into characters to print (see below)
  * if omitted, the program looks for printable ASCII characters (`0x20`&ndash;`0x7e`)

### *input_file*
* The binary file to find strings from.

### Table files
* format: UTF-8
* empty lines are ignored
* each line consists of:
  * a byte in the input file as two hexadecimal digits (`00`&ndash;`ff`)
  * a space
  * the character to print, or a hexadecimal Unicode codepoint (`00`&ndash;`10ffff`, at least two digits)

## Examples
```
python findstrings.py test\doom2.exe
0x025c: DOS/4G  Copyright (C) Rational Systems, Inc. 1987 - 1993
0x0c7c: DOS16M.386
(snip)
```

```
python findstrings.py --table-file tables\nes-smb1.txt --minimum-length 20 test\smb1.nes
0x07d2: LWELCOME TO WARP ZONE!
0x0d8e: MBUT OUR PRINCESS IS IN
(snip)
```
