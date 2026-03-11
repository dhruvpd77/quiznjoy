#!/bin/bash
# Run this on PythonAnywhere Bash console to fetch latest code
# Your username: dhruvpython

set -e
cd ~

echo "=== Step 1: Backup your data ==="
mkdir -p ~/quiznjoy_backup
[ -d ~/quiznjoy/media ] && cp -r ~/quiznjoy/media ~/quiznjoy_backup/ && echo "  Backed up media"
[ -f ~/quiznjoy/db.sqlite3 ] && cp ~/quiznjoy/db.sqlite3 ~/quiznjoy_backup/ && echo "  Backed up database"
[ -d ~/quiznjoy/static ] && cp -r ~/quiznjoy/static ~/quiznjoy_backup/ 2>/dev/null || true

echo "=== Step 2: Clone fresh from GitHub ==="
rm -rf ~/quiznjoy_old
mv ~/quiznjoy ~/quiznjoy_old 2>/dev/null || true
git clone https://github.com/dhruvpd77/quiznjoy.git
cd ~/quiznjoy

echo "=== Step 3: Restore your data ==="
[ -d ~/quiznjoy_backup/media ] && cp -r ~/quiznjoy_backup/media ~/quiznjoy/ && echo "  Restored media"
[ -f ~/quiznjoy_backup/db.sqlite3 ] && cp ~/quiznjoy_backup/db.sqlite3 ~/quiznjoy/ && echo "  Restored database"

echo "=== Step 4: Setup virtualenv ==="
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "=== Step 5: Django setup ==="
python manage.py migrate
python manage.py collectstatic --noinput

echo ""
echo "=== DONE! ==="
echo "Go to Web tab -> Reload your app"
echo ""
