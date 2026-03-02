# This file is for PythonAnywhere deployment
# Place this in your home directory on PythonAnywhere

import sys
import os

# Add your project directory to the path
path = '/home/yourusername/B4-QUIZ'  # CHANGE 'yourusername' to your PythonAnywhere username
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

