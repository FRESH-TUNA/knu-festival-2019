from django.conf import settings
from .base import *
import os

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ROOT_URLCONF = 'config.urls.production'

WSGI_APPLICATION = 'config.wsgi.production'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
