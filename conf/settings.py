"""
Django settings for dssg project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CATEGORIES_DIR = os.path.join(BASE_DIR, 'categories')
CATEGORY_CONFIG_FILENAME = 'category-config.json'
POST_TEMPLATE_NAME = 'post.html'
POSTS_DIR_NAME = 'posts'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
PAGES_DIR = os.path.join(TEMPLATES_DIR, 'pages')
INCLUDES_DIR = os.path.join(TEMPLATES_DIR, 'includes')

STATIC_DIR_NAME = 'static'
STATIC_DIR = os.path.join(BASE_DIR, STATIC_DIR_NAME)

OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_BACKUP_DIR = os.path.join(BASE_DIR, 'output-backup')

AUTHOR_DEFAULT = "Anonymous"
PUBLISHED_DEFAULT = True       # makemigrations and migrate on change
URL_PREFIX = "localhost:8080"  # no trailing slash
STATIC_URL = os.path.join(URL_PREFIX, STATIC_DIR_NAME) + '/'

TEMPLATE_DIRS = (
    CATEGORIES_DIR,
    TEMPLATES_DIR,
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jj%c_uzt#gz7i486qo60u6pk49d1+wd*%8-i2qfr9s+_^08c45'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'dssg',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
