"""
Default dssg configuration values.

These are overridden by a config.py if it exists.
"""

import os
import sys

from utils.simplog import info, warn, error


SOURCE_DIR = sys.argv[1]
CONFIGURATION_FILE = 'config.py'


URL_PREFIX = ''
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


config_file_path = os.path.join(SOURCE_DIR, CONFIGURATION_FILE)
if os.path.isfile(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config_file_text = config_file.read()
    try:
        exec(compile(config_file_text, "config.py", 'exec'))
    except Exception as e:
        error('Failed to import CONFIGURATION_FILE', e, config_file_path)
    info('Imported configuration file', config_file_path)
