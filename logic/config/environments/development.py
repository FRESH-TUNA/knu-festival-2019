from .base import *
import os
DEBUG = True
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# CONFIG_SECRET_DIR = os.path.join(BASE_DIR, '.credential')
# CONFIG_SETTINGS_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'devDBCredential.json')
# config_devdb_secret = json.loads(open(CONFIG_SETTINGS_COMMON_FILE).read())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ROOT_URLCONF = 'config.urls.development'
#media 설정

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

# sass settings #default로 static_root에 결과물을 저장한다.
SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'temp')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder'
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
