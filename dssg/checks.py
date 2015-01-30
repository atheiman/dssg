"""
Checks to be performed before dssg generation process.

Check functions are wrapped by check_all(). Check functions should return an
error message as soon as an error is encountered.
"""

import sys
import os
import fnmatch

from .defaults import *


MSG = "Error in source directory:\n"


def check_all(source_dir):
    """
    Check functions return an error message if failed.
    """
    checks = [
        check_source_dir(source_dir),
        check_categories_dir(os.path.join(source_dir, CATEGORIES_DIR)),
        check_templates_dir(os.path.join(source_dir, TEMPLATES_DIR)),
    ]
    errors = []
    for check_result in checks:
        if check_result:
            raise SystemExit(MSG + check_result)


def check_source_dir(source_d):
    c_exists = True if CATEGORIES_DIR in os.listdir(source_d) else False
    t_exists = True if TEMPLATES_DIR in os.listdir(source_d) else False
    if c_exists and not os.path.isdir(os.path.join(source_d, CATEGORIES_DIR)):
        return MSG + 'CATEGORIES_DIR is not a directory [{d}]'.format(
            d=os.path.join(source_d, CATEGORIES_DIR)
        )
    if t_exists and not os.path.isdir(os.path.join(source_d, TEMPLATES_DIR)):
        return MSG + 'TEMPLATES_DIR is not a directory [{d}]'.format(
                d=os.path.join(source_d, TEMPLATES_DIR)
        )

    c_empty = not bool(os.listdir(os.path.join(source_d, CATEGORIES_DIR)))
    t_empty = not bool(os.listdir(os.path.join(source_d, TEMPLATES_DIR)))
    msg = "Either CATEGORIES_DIR or TEMPLATES_DIR must exist and not be empty."
    if (not c_exists or c_empty) and (not t_exists or t_empty):
        return MSG + msg
    if (not t_exists or t_empty) and (not c_exists or c_empty):
        return MSG + msg


def check_categories_dir(categories_dir):
    # categories dir not required
    if not os.path.isdir(categories_dir):
        return

    for category_dn in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category_dn)
        if not os.path.isdir(category_dir):
            return (MSG +
                    "Non directory found in CATEGORIES_DIR "
                    "[{d}]".format(d=category_dir))

        if POSTS_DIR in os.listdir(category_dir):
            posts_dir = os.path.join(category_dir, POSTS_DIR)
            p_template_exists = False
            p_template_needed = bool(os.listdir(posts_dir))
            for post_fn in os.listdir(posts_dir):
                if os.path.splitext(post_fn)[1] != '.md':
                    return (MSG +
                            "File without .md extension found in POSTS_DIR "
                            "[{f}]".format(f=os.path.join(category_dir,
                                                          POSTS_DIR,
                                                          post_fn)))
            for fn in os.listdir(os.path.join(category_dir)):
                if fnmatch.fnmatch(fn, POST_TEMPLATES_MATCH):
                    p_template_exists = True
                    break
            if not p_template_exists and p_template_needed:
                return (MSG +
                        "No post template found matching POST_TEMPLATES_MATCH"
                        " in category directory [{dir}]".format(category_dir))


def check_templates_dir(templates_dir):
    if not os.path.isdir(templates_dir):
        # categories dir not required
        return
    return
