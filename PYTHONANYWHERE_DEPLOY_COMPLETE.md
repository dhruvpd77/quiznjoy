# 🚀 Complete PythonAnywhere Deployment Guide

## Step-by-Step Deployment for QuizNjoy with AI Features

---

## 📋 Prerequisites

1. **PythonAnywhere Account**: Sign up at https://www.pythonanywhere.com (Free tier works!)
2. **GitHub Repository**: Your code should be on GitHub
3. **Groq API Key**: Get free key at https://console.groq.com/keys (for AI solutions)

---

## 🔧 Step 1: Sign Up / Log In

1. Go to https://www.pythonanywhere.com
2. Sign up for a free account (or log in)
3. **Note your username** (e.g., `dhruvpd77`)

---

## 📥 Step 2: Clone Your Repository

1. Click **"Consoles"** tab → Click **"Bash"**
2. Run these commands:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git B4-QUIZ
cd B4-QUIZ
```

**OR** if you don't have GitHub:
1. Go to **"Files"** tab
2. Upload your project files to `/home/yourusername/B4-QUIZ/`

---

## 🐍 Step 3: Set Up Virtual Environment

```bash
cd ~/B4-QUIZ
python3.10 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 4: Install Dependencies

```bash
pip install --user -r requirements.txt
```

**Important**: The `--user` flag is required on PythonAnywhere free accounts.

---

## 🗄️ Step 5: Set Up Database

```bash
python manage.py migrate
```

This creates all database tables.

---

## 👤 Step 6: Create Admin User

```bash
python manage.py createsuperuser
```

Enter:
- Username: (your choice)
- Email: (optional)
- Password: (choose strong password)

---

## 📁 Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This collects all CSS, JavaScript, and images.

---

## ⚙️ Step 8: Configure Web App

1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"** (or edit existing)
3. Choose **"Manual configuration"**
4. Select **Python 3.10** (or your version)
5. Click **"Next"**

---

## 🔧 Step 9: Configure WSGI File

1. In **"Web"** tab, find **"WSGI configuration file"**
2. Click the file link (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all content** and paste this:

```python
import sys
import os

# Add your project directory to the path
path = '/home/yourusername/B4-QUIZ'
if path not in sys.path:
    sys.path.insert(0, path)

# Add virtual environment to path
venv_path = '/home/yourusername/B4-QUIZ/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `yourusername` with your actual PythonAnywhere username!**

4. **Save** the file

---

## 📂 Step 10: Configure Static Files

1. In **"Web"** tab, scroll to **"Static files"** section
2. Click **"Add a new mapping"**
3. Enter:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/B4-QUIZ/staticfiles`
4. Click **"Add"**

---

## 🖼️ Step 11: Configure Media Files

1. Still in **"Static files"** section
2. Click **"Add a new mapping"** again
3. Enter:
   - **URL**: `/media/`
   - **Directory**: `/home/yourusername/B4-QUIZ/media`
4. Click **"Add"**

---

## 🔑 Step 12: Set Environment Variables (For AI API)

1. In **"Web"** tab, scroll to **"Environment variables"** section
2. Add these variables:

```
GROQ_API_KEY=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
AI_PROVIDER=groq
```

**OR** you can keep them in `settings.py` (already configured)

---

## 🔄 Step 13: Reload Web App

1. In **"Web"** tab, click the big green **"Reload"** button
2. Wait 10-20 seconds for reload to complete

---

## ✅ Step 14: Test Your Website

1. Visit: `https://yourusername.pythonanywhere.com`
2. You should see the login page!
3. Log in with your superuser account
4. Test all features:
   - Create semesters/subjects
   - Upload questions
   - Take quizzes
   - Test "Understand Solution" button (AI feature)

---

## 🎯 Post-Deployment Checklist

- [ ] Website loads at `yourusername.pythonanywhere.com`
- [ ] Can log in with superuser
- [ ] Static files (CSS, images) load correctly
- [ ] Can create semesters and subjects
- [ ] Can upload questions via Excel
- [ ] Can take quizzes
- [ ] Quiz results show correctly
- [ ] "Understand Solution" button works (AI feature)
- [ ] Media files (question images) display
- [ ] Mobile view works properly

---

## 🔧 Troubleshooting

### Issue: "500 Internal Server Error"

**Solution:**
1. Check **"Error log"** in **"Web"** tab
2. Common fixes:
   - Wrong path in WSGI (check username)
   - Missing packages: `pip install --user -r requirements.txt`
   - Database not migrated: `python manage.py migrate`
   - Static files not collected: `python manage.py collectstatic`

### Issue: "Static files not loading"

**Solution:**
1. Run: `python manage.py collectstatic --noinput`
2. Check Static files mapping in Web tab
3. Verify paths are correct (no typos)
4. Reload web app

### Issue: "AI Solution not working"

**Solution:**
1. Check Groq API key is set in environment variables or settings.py
2. Verify `AI_PROVIDER = 'groq'` in settings
3. Check error log for API errors
4. Test API key at https://console.groq.com/keys

### Issue: "Media files not displaying"

**Solution:**
1. Check Media files mapping in Web tab
2. Verify `/media/` URL and directory path
3. Ensure media folder exists: `mkdir -p ~/B4-QUIZ/media`
4. Check file permissions

### Issue: "Module not found"

**Solution:**
1. Activate virtual environment: `source venv/bin/activate`
2. Install missing package: `pip install --user package_name`
3. Verify WSGI file has correct paths
4. Check error log for specific module name

---

## 🔄 Updating Your Website

When you make code changes:

```bash
cd ~/B4-QUIZ
git pull origin main  # or your branch name
source venv/bin/activate
pip install --user -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then **reload** web app in **"Web"** tab.

---

## 🔐 Security Notes

1. **SECRET_KEY**: Consider using environment variables
2. **DEBUG**: Automatically `False` on PythonAnywhere
3. **ALLOWED_HOSTS**: Already configured for your domain
4. **API Keys**: Keep them secure, use environment variables in production

---

## 📝 Important Paths

- **Project**: `/home/yourusername/B4-QUIZ`
- **Static Files**: `/home/yourusername/B4-QUIZ/staticfiles`
- **Media Files**: `/home/yourusername/B4-QUIZ/media`
- **WSGI File**: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- **Virtual Env**: `/home/yourusername/B4-QUIZ/venv`

---

## 🎉 Success!

Your QuizNjoy website is now live at:
**https://yourusername.pythonanywhere.com**

Features available:
- ✅ Quiz taking
- ✅ Admin dashboard
- ✅ Question management
- ✅ AI-powered solutions (Groq)
- ✅ Mobile-responsive design

---

## 📞 Need Help?

- **Error Logs**: Web tab → Error log
- **PythonAnywhere Docs**: https://help.pythonanywhere.com/
- **Django Docs**: https://docs.djangoproject.com/

**Good luck! 🚀**

