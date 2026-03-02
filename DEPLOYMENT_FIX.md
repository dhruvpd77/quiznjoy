# 🚀 Deployment Fix Guide - Fix "Rocket Page" Issue

## ✅ Issues Fixed:

1. **Static Files Configuration**: Fixed `STATIC_URL` to use `/static/` (with leading slash)
2. **Added Static Files Finders**: Ensures Django can find static files
3. **URL Configuration**: Updated to properly handle static files

## 📋 Deployment Checklist:

### Step 1: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

### Step 4: For PythonAnywhere - Configure Web App

1. **Go to Web Tab** in PythonAnywhere dashboard
2. **Static files mapping**:
   - URL: `/static/`
   - Directory: `/home/yourusername/B4-QUIZ/staticfiles`
3. **Media files mapping**:
   - URL: `/media/`
   - Directory: `/home/yourusername/B4-QUIZ/media`
4. **WSGI file path**: `/home/yourusername/B4-QUIZ/quiz_project/wsgi.py`
5. **Reload Web App**

### Step 5: Check ALLOWED_HOSTS

In `settings.py`, make sure `ALLOWED_HOSTS` includes your domain:
- For PythonAnywhere: `['yourusername.pythonanywhere.com']`
- Or use: `ALLOWED_HOSTS = ['*']` for testing (not recommended for production)

## 🔧 Common Issues & Fixes:

### Issue: Still seeing rocket page
**Fix**: 
- Check error logs in PythonAnywhere → Web tab → Error log
- Verify WSGI file path is correct
- Ensure `collectstatic` was run
- Check that static files mapping is configured

### Issue: 404 errors
**Fix**:
- Verify URLs are correct in `quiz_project/urls.py`
- Check that all apps are in `INSTALLED_APPS`
- Ensure migrations are applied

### Issue: Static files not loading
**Fix**:
- Run `python manage.py collectstatic`
- Configure static files mapping in web server
- Check `STATIC_ROOT` path is correct

### Issue: Database errors
**Fix**:
- Run `python manage.py migrate`
- Check database file permissions
- Ensure `db.sqlite3` is in the project root

## 🎯 Quick Test Commands:

```bash
# Test if Django can find all apps
python manage.py check

# Test if static files are configured
python manage.py collectstatic --dry-run

# Test if URLs are working
python manage.py show_urls  # (if django-extensions installed)
```

## 📝 Important Notes:

1. **Never commit SECRET_KEY** - Use environment variables in production
2. **Set DEBUG = False** in production
3. **Use proper ALLOWED_HOSTS** - Don't use `['*']` in production
4. **Collect static files** before deploying
5. **Run migrations** on the server

## ✅ After Deployment:

1. Visit your site: `https://yourusername.pythonanywhere.com`
2. Should redirect to login page (not rocket page)
3. Test login/signup
4. Test quiz functionality
5. Check admin panel works

---

**If you still see the rocket page after these fixes, check the error logs in PythonAnywhere Web tab!**

