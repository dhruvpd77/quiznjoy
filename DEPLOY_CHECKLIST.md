# ✅ PythonAnywhere Deployment Checklist

## Quick Reference - Copy & Paste Commands

### 1. Initial Setup (Bash Console)

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git B4-QUIZ
cd B4-QUIZ
python3.10 -m venv venv
source venv/bin/activate
pip install --user -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 2. Web App Configuration (Web Tab)

**WSGI File** - Replace content with:
```python
import sys
import os
path = '/home/YOUR_USERNAME/B4-QUIZ'
if path not in sys.path:
    sys.path.insert(0, path)
venv_path = '/home/YOUR_USERNAME/B4-QUIZ/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static Files Mapping:**
- URL: `/static/`
- Directory: `/home/YOUR_USERNAME/B4-QUIZ/staticfiles`

**Media Files Mapping:**
- URL: `/media/`
- Directory: `/home/YOUR_USERNAME/B4-QUIZ/media`

**Environment Variables (Optional):**
- `GROQ_API_KEY` = `your-groq-api-key`
- `AI_PROVIDER` = `groq`

### 3. After Configuration

1. Click **"Reload"** button in Web tab
2. Visit: `https://YOUR_USERNAME.pythonanywhere.com`
3. Test login and features

### 4. Common Issues Fix

```bash
# If static files not loading
python manage.py collectstatic --noinput

# If database errors
python manage.py migrate

# If missing packages
pip install --user -r requirements.txt

# Then reload web app
```

---

## ✅ Verification Checklist

- [ ] Website loads (not 500 error)
- [ ] Can log in
- [ ] CSS/images load (not broken)
- [ ] Can create semesters
- [ ] Can upload questions
- [ ] Can take quiz
- [ ] Quiz results show
- [ ] "Understand Solution" works
- [ ] Mobile view works

---

**Full Guide**: See `PYTHONANYWHERE_DEPLOY_COMPLETE.md`

