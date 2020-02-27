@echo off
cls

echo === test.bat: doom2.exe ===
python findstrings.py --minimum-length 20 --maximum-repeat 2 test\doom2.exe
echo.

echo === test.bat: smb1.nes ===
python findstrings.py --table-file tables\nes-smb1.txt --minimum-length 10 --maximum-repeat 3 test\smb1.nes
echo.

echo === test.bat: smb2.nes ===
python findstrings.py --table-file tables\nes-smb2.txt --minimum-length 5 --maximum-repeat 3 test\smb2.nes
echo.

echo === test.bat: smb3.nes ===
python findstrings.py --table-file tables\nes-smb3.txt --minimum-length 9 --maximum-repeat 8 test\smb3.nes
