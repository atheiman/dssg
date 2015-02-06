"""
Tools to write to output directory.
"""

import os
import shutil

from django.conf import settings

from dssg.static_site_app.models import Post, Category
from dssg.utils.simplog import info, warn, error


def build_output_tree(source_dir):
    # make an empty output dir
    os.mkdir(settings.OUTPUT_DIR)

    # copy the static dir to the output
    if os.path.isdir(os.path.join(source_dir, settings.STATIC_DIR)):
        info('Copying static directory to output', settings.STATIC_DIR)
        shutil.copytree(os.path.join(source_dir, settings.STATIC_DIR),
                        os.path.join(settings.OUTPUT_DIR, settings.STATIC_DIR))

    # make an empty directory for each category
    categories_dir = os.path.join(source_dir, settings.CATEGORIES_DIR)
    for c_dirname in os.listdir(categories_dir):
        info('Creating category directory in output', c_dirname)
        if os.path.isdir(os.path.join(categories_dir, c_dirname)):
            os.mkdir(os.path.join(settings.OUTPUT_DIR, c_dirname))


def write_file(path, contents):
    if os.path.isfile(path):
        warn('Writing to existing file', path)
    with open(path, 'w') as f:
        f.write(contents)


def write_category_page(page_dict, category):
    """
    Write a page_dict to the output_dir in the correct category.

    page_dict should be:

        {
            'source': 'template string output',
            'filename': 'filename' + '.ext',
        }

    category should be an instance of Category model.
    """
    out_file = os.path.join(settings.OUTPUT_DIR,
                            category.slug,
                            page_dict['filename'])
    info('Writing category page', out_file)
    write_file(out_file, page_dict['source'])


def write_post(post, post_files):
    """
    Write a post from each post_file dict:

        {
            'source': 'template string output',
            'filename': 'filename' + '.ext',
        }

    """
    info('Writing post', post)
    for p_file in post_files:
        out_file = os.path.join(settings.OUTPUT_DIR,
                                post.category.slug,
                                p_file['filename'])
        info('Writing post to post file in output', [post, p_file['filename']])
        write_file(out_file, p_file['source'])


def write_pages(page_file_dicts):
    """
    Write a page from each page_file dict:

        {
            'source': 'template string output',
            'filename': 'filename' + '.ext',
        }

    """
    for page_file in page_file_dicts:
        out_file = os.path.join(settings.OUTPUT_DIR, page_file['filename'])
        info('Writing page to page file in output', page_file['filename'])
        write_file(out_file, page_file['source'])
