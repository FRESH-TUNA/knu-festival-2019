from django.conf import settings
from .base import *
import os

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

ROOT_URLCONF = 'config.urls.staging'

WSGI_APPLICATION = 'config.wsgi.staging'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
