clear

echo "=== doom.exe ==="
python3 findstrings.py -l 20 test/doom.exe
echo

echo "=== nigel.nes ==="
python3 findstrings.py -t tables/nes-nigel.txt -l 8 -r 2 test/nigel.nes
echo

echo "=== smb1.nes ==="
python3 findstrings.py -t tables/nes-smb1.txt -l 10 -r 3 test/smb1.nes
echo

echo "=== smb2.nes ==="
python3 findstrings.py -t tables/nes-smb2.txt -r 3 test/smb2.nes
echo

echo "=== smb3.nes ==="
python3 findstrings.py -t tables/nes-smb3.txt -l 10 test/smb3.nes
echo

echo "=== smb3.nes, -d10 ==="
python3 findstrings.py -t tables/nes-smb3.txt -d 10 test/smb3.nes
echo

echo "=== repeat.txt, -r3, CSV ==="
python3 findstrings.py -r 3 -c test/repeat.txt
echo

echo "=== repeat.txt, -r4 ==="
python3 findstrings.py -r 4 test/repeat.txt
echo

echo "=== empty ==="
python3 findstrings.py test/empty
echo

echo "=== These should cause five distinct argument errors ==="
python3 findstrings.py -l 0 test/empty
python3 findstrings.py -d 0 test/empty
python3 findstrings.py -r 0 test/empty
python3 findstrings.py nonexistent
python3 findstrings.py -t nonexistent test/empty
echo

echo "=== These should cause four distinct table file errors ==="
python3 findstrings.py -t tables/error-utf16.txt test/empty
python3 findstrings.py -t tables/error-syntax.txt test/empty
python3 findstrings.py -t tables/error-hex.txt test/empty
python3 findstrings.py -t tables/error-range.txt test/empty
echo
