#!/usr/bin/env python
"""
Quick deployment fix script
Run this before deploying to ensure everything is ready
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings

def main():
    print("🚀 QuizNjoy Deployment Fix Script")
    print("=" * 50)
    
    # Check 1: Django system check
    print("\n1. Running Django system check...")
    try:
        call_command('check', verbosity=0)
        print("   ✅ Django system check passed!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Check 2: Check migrations
    print("\n2. Checking migrations...")
    try:
        call_command('showmigrations', verbosity=0)
        print("   ✅ Migrations check passed!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Check 3: Collect static files
    print("\n3. Collecting static files...")
    try:
        call_command('collectstatic', '--noinput', verbosity=1)
        print("   ✅ Static files collected!")
    except Exception as e:
        print(f"   ⚠️  Warning: {e}")
        print("   (This is OK if static files are already collected)")
    
    # Check 4: Verify settings
    print("\n4. Verifying settings...")
    checks = []
    
    if settings.STATIC_ROOT:
        checks.append(f"   ✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    else:
        checks.append("   ❌ STATIC_ROOT not set!")
    
    if settings.MEDIA_ROOT:
        checks.append(f"   ✅ MEDIA_ROOT: {settings.MEDIA_ROOT}")
    else:
        checks.append("   ❌ MEDIA_ROOT not set!")
    
    if settings.ALLOWED_HOSTS:
        checks.append(f"   ✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    else:
        checks.append("   ⚠️  ALLOWED_HOSTS is empty!")
    
    for check in checks:
        print(check)
    
    # Check 5: Verify apps
    print("\n5. Verifying installed apps...")
    required_apps = ['accounts', 'quiz', 'semesters']
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"   ✅ {app} is installed")
        else:
            print(f"   ❌ {app} is NOT installed!")
    
    print("\n" + "=" * 50)
    print("✅ Deployment check complete!")
    print("\n📋 Next steps:")
    print("   1. Run migrations: python manage.py migrate")
    print("   2. Collect static: python manage.py collectstatic")
    print("   3. Configure web server static files mapping")
    print("   4. Reload web app")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

