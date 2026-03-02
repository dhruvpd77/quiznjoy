# PythonAnywhere Deployment Guide for QuizNjoy

Complete step-by-step guide to deploy your QuizNjoy Django project on PythonAnywhere.com

## 📋 Prerequisites

1. **PythonAnywhere Account**: Sign up at https://www.pythonanywhere.com (Free tier available)
2. **GitHub Repository**: Your code should be on GitHub (already done ✅)
3. **Basic Terminal Knowledge**: Familiarity with command line

---

## 🚀 Step-by-Step Deployment

### Step 1: Sign Up / Log In to PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Sign up for a free account (or log in if you have one)
3. Note your **username** (e.g., `dhruvpd77`)

---

### Step 2: Open Bash Console

1. Click on **"Consoles"** tab in the top menu
2. Click **"Bash"** to open a new console
3. You'll see a terminal prompt

---

### Step 3: Clone Your GitHub Repository

```bash
cd ~
git clone https://github.com/dhruvpd77/quiznjoy.git B4-QUIZ
cd B4-QUIZ
git checkout quiznjoyfinal
```

**Note**: Replace `dhruvpd77` with your GitHub username if different.

---

### Step 4: Create Virtual Environment

```bash
cd ~/B4-QUIZ
python3.10 -m venv venv
source venv/bin/activate
```

**Note**: PythonAnywhere uses Python 3.10 by default. Adjust if needed.

---

### Step 5: Install Dependencies

```bash
pip install --user -r requirements.txt
```

**Important**: Use `--user` flag on PythonAnywhere free accounts.

---

### Step 6: Set Up Database

```bash
python manage.py migrate
```

This will create the database tables.

---

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Enter:
- Username: (your choice)
- Email: (optional)
- Password: (choose a strong password)

---

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This collects all CSS, JavaScript, and images into the `staticfiles` folder.

---

### Step 9: Configure Web App

1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10** (or your Python version)
5. Click **"Next"**

---

### Step 10: Configure WSGI File

1. In the **"Web"** tab, find **"WSGI configuration file"**
2. Click on the file link (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all existing content**
4. **Paste this code** (replace `yourusername` with your PythonAnywhere username):

```python
import sys
import os

# Add your project directory to the path
path = '/home/yourusername/B4-QUIZ'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. **Save the file**

---

### Step 11: Configure Static Files Mapping

1. In the **"Web"** tab, scroll to **"Static files"** section
2. Click **"Add a new mapping"**
3. **URL**: `/static/`
4. **Directory**: `/home/yourusername/B4-QUIZ/staticfiles`
5. Click **"Add"**

---

### Step 12: Configure Media Files Mapping

1. Still in **"Static files"** section
2. Click **"Add a new mapping"** again
3. **URL**: `/media/`
4. **Directory**: `/home/yourusername/B4-QUIZ/media`
5. Click **"Add"**

---

### Step 13: Reload Web App

1. In the **"Web"** tab, click the big green **"Reload"** button
2. Wait for the reload to complete (usually 10-20 seconds)

---

### Step 14: Test Your Website

1. Your website URL will be: `https://yourusername.pythonanywhere.com`
2. Open it in a browser
3. You should see the QuizNjoy login page!

---

## ✅ Post-Deployment Checklist

- [ ] Website loads correctly
- [ ] Can log in with superuser account
- [ ] Static files (CSS, images) load properly
- [ ] Can create semesters and subjects
- [ ] Can upload questions via Excel
- [ ] Can take quizzes
- [ ] Media files (question images) display correctly

---

## 🔧 Troubleshooting

### Issue: "500 Internal Server Error"

**Solution:**
1. Check **"Error log"** in the **"Web"** tab
2. Common issues:
   - Wrong path in WSGI file (check your username)
   - Missing dependencies (run `pip install --user -r requirements.txt`)
   - Database not migrated (run `python manage.py migrate`)

### Issue: "Static files not loading"

**Solution:**
1. Make sure you ran `python manage.py collectstatic`
2. Check Static files mapping in Web tab
3. Verify paths are correct (no typos)

### Issue: "Media files not displaying"

**Solution:**
1. Check Media files mapping in Web tab
2. Verify `/media/` URL and `/home/yourusername/B4-QUIZ/media` directory path
3. Make sure media folder has correct permissions

### Issue: "Module not found"

**Solution:**
1. Check virtual environment is activated
2. Install missing packages: `pip install --user package_name`
3. Verify WSGI file has correct path

### Issue: "Database locked"

**Solution:**
1. This can happen with SQLite on PythonAnywhere
2. Consider upgrading to MySQL (available on paid plans)
3. Or ensure only one process accesses the database at a time

---

## 🔄 Updating Your Website

When you make changes to your code:

```bash
cd ~/B4-QUIZ
git pull origin quiznjoyfinal
source venv/bin/activate
pip install --user -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then **reload** your web app in the **"Web"** tab.

---

## 🔐 Security Notes

1. **SECRET_KEY**: Consider using environment variables for production
2. **DEBUG**: Already set to `False` on PythonAnywhere automatically
3. **ALLOWED_HOSTS**: Already configured for your PythonAnywhere domain
4. **Database**: SQLite works for small projects, but consider MySQL for production

---

## 📝 Important Paths on PythonAnywhere

- **Project Directory**: `/home/yourusername/B4-QUIZ`
- **Static Files**: `/home/yourusername/B4-QUIZ/staticfiles`
- **Media Files**: `/home/yourusername/B4-QUIZ/media`
- **WSGI File**: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- **Virtual Environment**: `/home/yourusername/B4-QUIZ/venv`

---

## 🎉 Success!

Your QuizNjoy website should now be live at:
**https://yourusername.pythonanywhere.com**

---

## 📞 Need Help?

- PythonAnywhere Docs: https://help.pythonanywhere.com/
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Check Error Logs: Web tab → Error log

---

**Good luck with your deployment! 🚀**

