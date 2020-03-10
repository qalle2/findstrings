@echo off
cls

echo === test.bat: doom2.exe ===
python findstrings.py --minimum-length 20 --maximum-repeat 2 test\doom2.exe
if errorlevel 1 goto error
echo.

echo === test.bat: smb1.nes ===
python findstrings.py --table-file tables\nes-smb1.txt --minimum-length 10 --maximum-repeat 3 test\smb1.nes
if errorlevel 1 goto error
echo.

echo === test.bat: smb2.nes ===
python findstrings.py --table-file tables\nes-smb2.txt --minimum-length 5 --maximum-repeat 3 test\smb2.nes
if errorlevel 1 goto error
echo.

echo === test.bat: smb3.nes ===
python findstrings.py --table-file tables\nes-smb3.txt --minimum-length 9 --maximum-repeat 8 --start-quote "`" --end-quote "'" test\smb3.nes
if errorlevel 1 goto error
echo.

echo === test.bat: help ===
python findstrings.py --help
if errorlevel 1 goto error
echo.

echo === test.bat: all of these should cause an error ===
python findstrings.py
if not errorlevel 1 goto missingerror
python findstrings.py --xxx test\doom2.exe
if not errorlevel 1 goto missingerror
python findstrings.py --minimum-length "x" test\doom2.exe
if not errorlevel 1 goto missingerror
python findstrings.py --minimum-length 0 test\doom2.exe
if not errorlevel 1 goto missingerror
echo.

echo === test.bat: all tests passed ===
goto end

:error
echo === test.bat: error detected ===
goto end

:missingerror
echo === test.bat: lack of error detected ===
goto end

:end