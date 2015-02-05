"""
Django settings for static_site app used in dssg generation process.
"""

import os
import sys

from dssg.defaults import *

# BASE_DIR = abs/path/to/dssg
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(1, BASE_DIR)


SECRET_KEY = 'some-secret-key'

DEBUG = True

TEMPLATE_DEBUG = True


INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'dssg.static_site_app',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)

ROOT_URLCONF = 'static_site.urls'

WSGI_APPLICATION = 'static_site.conf.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), TEMP_DB),
    }
}

TEMPLATE_DIRS = (
    os.path.join(SOURCE_DIR, CATEGORIES_DIR),
    os.path.join(SOURCE_DIR, TEMPLATES_DIR),
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False


STATIC_URL = '/'.join([URL_PREFIX, STATIC_DIR,]) + '/'
