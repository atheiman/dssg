"""
Checks to be performed before dssg generation process.
"""

import sys
import os
import fnmatch

from .defaults import *


MSG = "Errors in source directory:\n"


def check_wrapper():
    """
    Check functions return an error message if failed.
    """
    source_dir = sys.argv[1]
    errors = []
    checks_list = [
        check_source_dir(source_dir),
        check_categories_dir(os.path.join(source_dir, CATEGORIES_DIR)),
        check_templates_dir(os.path.join(source_dir, TEMPLATES_DIR)),
    ]
    for check_result in checks_list:
        errors.append(check_result)
    if errors:
        raise SystemExit(
            MSG +
            '\n\n'.join(errors)
        )


def check_source_dir(source_d):
    c_exists = True if CATEGORIES_DIR in os.listdir(source_d) else False
    t_exists = True if TEMPLATES_DIR in os.listdir(source_d) else False

    if c_exists and not os.path.isdir(os.path.join(source_d, CATEGORIES_DIR)):
        raise SystemExit(
            MSG +
            'CATEGORIES_DIR is not a directory [{d}]'.format(
                d=os.path.join(source_d, CATEGORIES_DIR))
        )
    if t_exists and not os.path.isdir(os.path.join(source_d, TEMPLATES_DIR)):
        raise SystemExit(
            MSG +
            'TEMPLATES_DIR is not a directory [{d}]'.format(
                d=os.path.join(source_d, TEMPLATES_DIR))
        )

    c_empty = bool(os.listdir(os.path.join(source_d, CATEGORIES_DIR)))
    t_empty = bool(os.listdir(os.path.join(source_d, TEMPLATES_DIR)))

    if (not c_exists or c_empty) and (not t_exists or t_empty):
        return "Either CATEGORIES_DIR or TEMPLATES_DIR must exist and not be empty."
    if (not t_exists or t_empty) and (not c_exists or c_empty):
        return "Either CATEGORIES_DIR or TEMPLATES_DIR must exist and not be empty."


def check_categories_dir(categories_dir):
    if not os.categories_dir


def source_dir_check():
    for category_dn in os.listdir(os.path.join(source_dir, CATEGORIES_DIR)):
        category_dir = os.path.join(source_dir, CATEGORIES_DIR, category_dn)
        if not os.path.isdir(category_dir):
            raise SystemExit(
                msg +
                "Non directory found in CATEGORIES_DIR:\n{d}".format(
                    d=category_dir)
            )

        if POSTS_DIR in os.listdir(category_dir):
            posts_dir = os.path.join(category_dir, POSTS_DIR)
            p_template_exists = False
            p_template_needed = bool(os.listdir(posts_dir))
            for post_fn in os.listdir(posts_dir):
                if os.path.splitext(post_fn)[1] != '.md':
                    raise SystemExit(
                        msg +
                        "Non post markdown source file found in POSTS_DIR:\n"
                        "{post_fn}".format(post_fn=os.path.join(category_dir,
                                                        POSTS_DIR, post_fn))
                    )
            for fn in os.listdir(os.path.join(category_dir)):
                if fnmatch.fnmatch(fn, POST_TEMPLATES_MATCH):
                    p_template_exists = True
                    break
            if not p_template_exists and p_template_needed:
                raise SystemExit(
                    msg +
                    "No post template found matching"
                    " POST_TEMPLATES_MATCH in {dir}".format(category_dir)
                )
