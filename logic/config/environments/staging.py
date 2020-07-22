from django.conf import settings
from .base import *
import os

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ROOT_URLCONF = 'config.urls.staging'

ALLOWED_HOSTS = [os.environ['WEB_HOST']]

WSGI_APPLICATION = 'config.wsgi.staging'
