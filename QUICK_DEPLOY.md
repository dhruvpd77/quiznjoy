# Quick PythonAnywhere Deployment - Cheat Sheet

## 🚀 Fast Track (5 Minutes)

### 1. Clone & Setup
```bash
cd ~
git clone https://github.com/dhruvpd77/quiznjoy.git B4-QUIZ
cd B4-QUIZ
git checkout quiznjoyfinal
python3.10 -m venv venv
source venv/bin/activate
pip install --user -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 2. Web Tab Configuration

**WSGI File** (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):
```python
import sys
import os
path = '/home/yourusername/B4-QUIZ'
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static Files Mapping:**
- URL: `/static/`
- Directory: `/home/yourusername/B4-QUIZ/staticfiles`

**Media Files Mapping:**
- URL: `/media/`
- Directory: `/home/yourusername/B4-QUIZ/media`

### 3. Reload & Done!
Click the green **"Reload"** button in Web tab.

Your site: `https://yourusername.pythonanywhere.com`

---

## 🔄 Update Commands

```bash
cd ~/B4-QUIZ
git pull origin quiznjoyfinal
source venv/bin/activate
pip install --user -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Then reload in Web tab.

---

## ⚠️ Common Issues

**500 Error?** → Check Error log in Web tab

**Static files broken?** → Run `collectstatic` again

**Media not showing?** → Check media mapping in Web tab

---

For detailed guide, see `PYTHONANYWHERE_DEPLOYMENT.md`

