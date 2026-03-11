# PythonAnywhere Setup from Scratch - QuizNjoy

Complete guide to deploy QuizNjoy from scratch. Replace `dhruvpython` with your PythonAnywhere username.

---

## Part 1: Bash Console (Clone & Setup)

Open **Consoles** → **Bash** and run these commands:

### Step 1: Clone the repository
```bash
cd ~
# If you have old quiznjoy folder, remove or rename it first:
# mv quiznjoy quiznjoy_old

git clone https://github.com/dhruvpd77/quiznjoy.git
cd ~/quiznjoy
```

### Step 2: Create virtual environment
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run migrations (creates database)
```bash
python manage.py migrate
```

### Step 5: Create admin user (optional but recommended)
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 6: Collect static files
```bash
python manage.py collectstatic --noinput
```

---

## Part 2: Web Tab Configuration

Go to **Web** tab on PythonAnywhere.

### 2.1 Add a new web app (if not exists)
- Click **Add a new web app**
- Choose **Manual configuration**
- Select **Python 3.10**

### 2.2 Code section
| Setting | Value |
|---------|-------|
| **Source code** | `/home/dhruvpython/quiznjoy` |
| **Working directory** | `/home/dhruvpython/quiznjoy` |

### 2.3 Virtualenv
- Click the link and enter: `/home/dhruvpython/quiznjoy/venv`

### 2.4 WSGI configuration file
Click the WSGI file link (e.g. `/var/www/dhruvpython_pythonanywhere_com_wsgi.py`) and **replace all content** with:

```python
import os
import sys

path = '/home/dhruvpython/quiznjoy'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Save the file.**

### 2.5 Static files mapping
In **Static files** section, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/dhruvpython/quiznjoy/staticfiles` |
| `/media/` | `/home/dhruvpython/quiznjoy/media` |

### 2.6 Environment variables (optional - for AI features)
In **Web** tab → **Environment variables** (or add in WSGI before `get_wsgi_application`):
- `GROQ_API_KEY` = your key from https://console.groq.com/keys
- `AI_PROVIDER` = `groq`

### 2.7 Reload
Click the green **Reload** button.

---

## Part 3: Create media folder (if needed)
```bash
mkdir -p ~/quiznjoy/media
```

---

## Your site URL
After setup: **https://dhruvpython.pythonanywhere.com**

---

## Future updates (after initial setup)
```bash
cd ~/quiznjoy
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Then click **Reload** in Web tab.
