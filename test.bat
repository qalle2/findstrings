@echo off
cls

echo === doom2.exe ===
python findstrings.py --minimum-length 20 test\doom2.exe
echo.

echo === smb1.nes ===
python findstrings.py --table-file tables\nes-smb1.txt --minimum-length 10 --maximum-repeat 3 test\smb1.nes
echo.

echo === smb2.nes ===
python findstrings.py --table-file tables\nes-smb2.txt --maximum-repeat 3 test\smb2.nes
echo.

echo === smb3.nes ===
python findstrings.py --table-file tables\nes-smb3.txt --minimum-length 10 test\smb3.nes
echo.

echo === repeat.txt ===
python findstrings.py --maximum-repeat 4 test\repeat.txt
echo.

echo === empty.dat ===
python findstrings.py test\empty.dat
echo.

echo === These should cause three errors ===
python findstrings.py
python findstrings.py --minimum-length "x" test\doom2.exe
python findstrings.py --minimum-length 0 test\doom2.exe
echo.

echo === Help text ===
python findstrings.py --help
