#!/bin/bash
# Run this on PythonAnywhere Bash console
# Replace dhruvpython with YOUR PythonAnywhere username

cd ~

# Remove old folder if exists (backup first if you have data)
[ -d quiznjoy ] && mv quiznjoy quiznjoy_backup_$(date +%Y%m%d) 2>/dev/null || true

# Clone from GitHub
git clone https://github.com/dhruvpd77/quiznjoy.git
cd quiznjoy

# Setup
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p media

echo ""
echo "=== DONE! ==="
echo "Now configure Web tab:"
echo "  Source: /home/dhruvpython/quiznjoy"
echo "  Working dir: /home/dhruvpython/quiznjoy"
echo "  Virtualenv: /home/dhruvpython/quiznjoy/venv"
echo "  Static: /static/ -> /home/dhruvpython/quiznjoy/staticfiles"
echo "  Media: /media/ -> /home/dhruvpython/quiznjoy/media"
echo "  Then click Reload"
echo ""
