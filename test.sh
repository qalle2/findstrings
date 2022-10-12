clear

echo "=== doom2.exe ==="
python3 findstrings.py -l 20 test/doom2.exe
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

echo "=== This should cause an error ==="
python3 findstrings.py -l 0 test/doom2.exe
echo
