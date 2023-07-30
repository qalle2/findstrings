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

echo "=== repeat.txt ==="
python3 findstrings.py -r 4 test/repeat.txt
echo

echo "=== empty.dat ==="
python3 findstrings.py test/empty.dat
echo

echo "=== These should cause four distinct errors ==="
python3 findstrings.py -l 0 test/empty.dat
python3 findstrings.py -t tables/error-utf16.txt test/empty.dat
python3 findstrings.py -t tables/error-syntax1.txt test/empty.dat
python3 findstrings.py -t tables/error-syntax2.txt test/empty.dat

echo
