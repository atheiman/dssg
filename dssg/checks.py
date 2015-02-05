"""
Checks to be performed before dssg generation process.

Check functions are wrapped by check_all(). Check functions should call error()
as soon as an error is encountered. Call warn() and info() as appropriate.

Two additional checks are performed in bin/dssg:

1.  len(sys.argv) == 2
2.  os.path.isdir(sys.argv[1])
"""

import os
import fnmatch
import shutil

from django.conf import settings

from .utils.simplog import error, warn, info


def check_all(source_dir):
    check_source_dir(source_dir),
    check_categories_dir(os.path.join(source_dir, settings.CATEGORIES_DIR)),
    check_templates_dir(os.path.join(source_dir, settings.TEMPLATES_DIR)),
    check_static_dir(os.path.join(source_dir, settings.STATIC_DIR)),
    check_output_dir(settings.OUTPUT_DIR),
    check_temp_db(settings.TEMP_DB),


def check_output_dir(output_dir):
    shutil.rmtree(settings.OUTPUT_BACKUP_DIR, ignore_errors=True)
    if os.path.isdir(output_dir) and os.listdir(output_dir):
        shutil.move(output_dir, settings.OUTPUT_BACKUP_DIR)
    shutil.rmtree(settings.OUTPUT_DIR, ignore_errors=True)


def check_temp_db(temp_db):
    if os.path.isfile(temp_db):
        os.remove(temp_db)
        warn('Removed TEMP_DB', temp_db)


def check_source_dir(source_dir):
    if not os.path.isdir(source_dir):
        error('Source directory is not a directory', source_dir)

    c_t_msg = ("Either CATEGORIES_DIR or TEMPLATES_DIR must exist "
               "and not be empty.")

    c_dir = os.path.join(source_dir, settings.CATEGORIES_DIR)
    if settings.CATEGORIES_DIR in os.listdir(source_dir) and os.listdir(c_dir):
        c_usable = True
    else:
        c_usable = False
    t_dir = os.path.join(source_dir, settings.TEMPLATES_DIR)
    if settings.TEMPLATES_DIR in os.listdir(source_dir) and os.listdir(t_dir):
        t_usable = True
    else:
        t_usable = False
    if not c_usable and not t_usable:
        error(c_t_msg)
    if not c_usable:
        warn('CATEGORIES_DIR not found or empty',
             os.path.join(source_dir, settings.CATEGORIES_DIR))
    if not t_usable:
        warn('TEMPLATES_DIR not found or empty',
             os.path.join(source_dir, settings.TEMPLATES_DIR))

    # get rid of c files that are sometimes generated when dir is tested
    if 'c' in os.listdir(source_dir):
        os.remove(os.path.join(source_dir, 'c'))
        warn('removed binary file', os.path.join(source_dir, 'c'))
    c_file = os.path.split(source_dir)[1] + 'c'
    if c_file in os.listdir(os.path.dirname(os.path.abspath(source_dir))):
        os.remove(c_file)
        warn('removed binary file', c_file)


def check_categories_dir(categories_dir):
    # categories dir not required
    if not os.path.isdir(categories_dir):
        return

    for category_dn in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category_dn)
        if not os.path.isdir(category_dir):
            error('Non directory found in CATEGORIES_DIR', category_dir)

        files = []
        for f in os.listdir(category_dir):
            if os.path.isdir(os.path.join(category_dir, f)):
                for f2 in os.listdir(os.path.join(category_dir, f)):
                    files.append(f2)
            files.append(f)
        if settings.POSTS_DIR in os.listdir(category_dir):
            posts_dir = os.path.join(category_dir, settings.POSTS_DIR)
            p_template_exists = False
            p_template_needed = bool(os.listdir(posts_dir))
            for post_fn in os.listdir(posts_dir):
                if os.path.splitext(post_fn)[1] != '.md':
                    error('File without .md extension found in POSTS_DIR',
                          os.path.join(category_dir, POSTS_DIR, post_fn))
            for fn in os.listdir(os.path.join(category_dir)):
                if fnmatch.fnmatch(fn, settings.POST_TEMPLATES_MATCH):
                    p_template_exists = True
                    break
            if not p_template_exists and p_template_needed:
                error('No post template found matching POST_TEMPLATES_MATCH',
                      category_dir)

        if len(files) != len(set(files)):
            error('Duplicate filenames within a category directory',
                  category_dir)


def check_templates_dir(templates_dir):
    # templates dir not required
    if not os.path.isdir(templates_dir):
        return

    dirs = os.listdir(templates_dir)

    if settings.INCLUDES_DIR not in dirs:
        warn('No includes directory found',
             os.path.join(templates_dir, settings.INCLUDES_DIR))

    if settings.PAGES_DIR not in dirs:
        warn('No pages directory found',
             os.path.join(templates_dir, settings.PAGES_DIR))

    for d in dirs:
        if d != settings.INCLUDES_DIR and d != settings.PAGES_DIR:
            error(
                ('Directory foung in TEMPLATES_DIR not matching INCLUDES_DIR'
                 ' or PAGES_DIR'),
                d
            )


def check_static_dir(static_dir):
    # static dir not required
    if not os.path.isdir(static_dir):
        warn('No static directory found', static_dir)
