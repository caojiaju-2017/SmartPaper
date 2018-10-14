"""
WSGI config for DisplayServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys
from os import sys, path
from django.core.wsgi import get_wsgi_application

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,PROJECT_DIR) # 5
os.sys.path.append(os.path.dirname(os.path.abspath('.')))

os.environ["DJANGO_SETTINGS_MODULE"] = "SmartPaperServer.settings"
application = get_wsgi_application()
