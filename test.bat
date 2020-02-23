@echo off
cls

echo === test.bat: doom2.exe ===
python findstrings.py --minimum-length 20 --maximum-repeat 2 test\doom2.exe
echo.

echo === test.bat: smb1.nes ===
python findstrings.py --minimum-length 12 --maximum-repeat 2 --table-file tables\nes-smb1.txt test\smb1.nes
echo.

echo === test.bat: smb3.nes ===
python findstrings.py --minimum-length 12 --maximum-repeat 8 --table-file tables\nes-smb3.txt test\smb3.nes
