"""
Default dssg configuration values.

These are overridden by a config.py if it exists.
"""

import os
import sys
import imp

from .utils.filesystem import get_abs_path


SOURCE_DIR = sys.argv[1]
CONFIGURATION_FILE = 'config.py'


URL_PREFIX = 'oh no'
GLOBAL_CONTEXT = {}
DEFAULT_POST_FILE_EXTENSION = '.html'
OUTPUT_DIR = 'output'
OUTPUT_BACKUP_DIR = 'output-backup'
CATEGORIES_DIR = 'categories'
CATEGORY_CONFIG_FILE = 'category-config.json'
POST_TEMPLATES_MATCH = 'post.*'
POSTS_DIR = 'posts'
TEMPLATES_DIR = 'templates'
INCLUDES_DIR = 'includes'
PAGES_DIR = 'pages'
STATIC_DIR = 'static'
AUTHOR_DEFAULT = 'Anonymous'
PUBLISHED_DEFAULT = True
DATE_INPUT_FORMATS = (
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',
    '%b %d %Y', '%b %d, %Y',
    '%d %b %Y', '%d %b, %Y',
    '%B %d %Y', '%B %d, %Y',
    '%d %B %Y', '%d %B, %Y',
)
DATE_FORMAT = 'N j, Y'
SHORT_DATE_FORMAT = 'm/d/Y'
TEMP_DB = 'db.sqlite3'


# print get_abs_path(SOURCE_DIR)
config_file_path = os.path.join(SOURCE_DIR, CONFIGURATION_FILE)
if os.path.isfile(os.path.join(SOURCE_DIR, CONFIGURATION_FILE)):
    config = imp.load_source('config.py', get_abs_path(SOURCE_DIR))
    print config
    from config import *

print URL_PREFIX
