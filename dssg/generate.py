"""
Script that wraps and steps through the dssg generation process.
"""

import os
import django
from django.core.management import call_command

from dssg.checks import check_all
from utils.simplog import info, warn, error


def generate(source_dir):
    """
    Generate static site from command line with command `dssg <source-dir>`
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dssg.django_conf.settings'
    django.setup()
    info('Running pre-generation checks')
    check_all(source_dir)
    info('Building temporary database')
    call_command('makemigrations', verbosity=0)
    call_command('makemigrations', 'static_site_app', verbosity=0)
    call_command('migrate', verbosity=0)
    from dssg.parsers import parse_source_dir
    parse_source_dir(source_dir)

