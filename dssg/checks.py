"""
Checks to be performed before dssg generation process.

Check functions are wrapped by check_all(). Check functions should return an
error message as soon as an error is encountered.
"""

import os
import fnmatch
import shutil

from .defaults import *


MSG = "ERROR - Source directory improper, correct the following issues:\n\t"


def check_all(source_dir):
    """
    Check functions return an error message if failed.
    """
    checks = [
        check_source_dir(source_dir),
        check_categories_dir(os.path.join(source_dir, CATEGORIES_DIR)),
        check_templates_dir(os.path.join(source_dir, TEMPLATES_DIR)),
        check_output_dir(OUTPUT_DIR),
        check_temp_db(TEMP_DB),
    ]
    errors = []
    for check_result in checks:
        if check_result:
            raise SystemExit(MSG + check_result)


def check_output_dir(output_dir):
    shutil.rmtree(OUTPUT_BACKUP_DIR, ignore_errors=True)
    if os.path.isdir(output_dir) and os.listdir(output_dir):
        shutil.move(output_dir, OUTPUT_BACKUP_DIR)
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)


def check_temp_db(temp_db):
    if os.path.isfile(temp_db):
        os.remove(temp_db)


def check_source_dir(source_d):
    if not os.path.isdir(source_d):
        return 'Source directory is not a directory [{d}]'.format(d=source_d)

    c_t_msg = ("Either CATEGORIES_DIR or TEMPLATES_DIR must exist "
               "and not be empty.")

    c_dir = os.path.join(source_d, CATEGORIES_DIR)
    if CATEGORIES_DIR in os.listdir(source_d) and os.listdir(c_dir):
        c_usable = True
    else:
        c_usable = False
    t_dir = os.path.join(source_d, TEMPLATES_DIR)
    if TEMPLATES_DIR in os.listdir(source_d) and os.listdir(t_dir):
        t_usable = True
    else:
        t_usable = False
    if not c_usable and not t_usable:
        return c_t_msg
    if not c_usable:
        print "WARNING - CATEGORIES_DIR not found or empty [{d}]".format(
            d=os.path.join(source_d, CATEGORIES_DIR)
        )
    if not t_usable:
        print "WARNING - TEMPLATES_DIR not found or empty [{d}]".format(
            d=os.path.join(source_d, TEMPLATES_DIR)
        )

    # get rid of 'c' files that are generated when dir is tested
    if 'c' in os.listdir(source_d):
        os.remove(os.path.join(source_d, 'c'))
        print 'removed binary file %s' % os.path.join(source_d, 'c')
    c_file = os.path.split(source_d)[1] + 'c'
    if c_file in os.listdir(os.path.dirname(os.path.abspath(source_d))):
        os.remove(c_file)
        print 'removed binary file %s' % c_file


def check_categories_dir(categories_dir):
    # categories dir not required
    if not os.path.isdir(categories_dir):
        return

    for category_dn in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category_dn)
        if not os.path.isdir(category_dir):
            return ("Non directory found in CATEGORIES_DIR "
                    "[{d}]".format(d=category_dir))

        if POSTS_DIR in os.listdir(category_dir):
            posts_dir = os.path.join(category_dir, POSTS_DIR)
            p_template_exists = False
            p_template_needed = bool(os.listdir(posts_dir))
            for post_fn in os.listdir(posts_dir):
                if os.path.splitext(post_fn)[1] != '.md':
                    return ("File without .md extension found in POSTS_DIR "
                            "[{f}]".format(f=os.path.join(category_dir,
                                                          POSTS_DIR,
                                                          post_fn)))
            for fn in os.listdir(os.path.join(category_dir)):
                if fnmatch.fnmatch(fn, POST_TEMPLATES_MATCH):
                    p_template_exists = True
                    break
            if not p_template_exists and p_template_needed:
                return ("No post template found matching POST_TEMPLATES_MATCH"
                        " in category directory [{dir}]".format(category_dir))


def check_templates_dir(templates_dir):
    if not os.path.isdir(templates_dir):
        # templates dir not required
        return
    return
