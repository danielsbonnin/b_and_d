"""
WSGI config for bAndD_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys


sys.path.append('/home/pi/bAndD_django/bAndD_django/bAndD_django')
sys.path.append('/home/pi/bAndD_django/bAndD_django/eb-virt/lib/python3.4/site-packages')
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bAndD_django.settings")

application = get_wsgi_application()
