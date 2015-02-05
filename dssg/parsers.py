"""
Parsers for reading in a source directory and saving objects to a database.
"""

import os
import shutil
import json
import fnmatch

import markdown
from django.utils.text import slugify
from django.template import Context
from django.template.loader import get_template
from django.conf import settings

from dssg.static_site_app.models import Post, Category
from dssg.utils.simplog import error, warn, info


def parse_source_dir(source_dir):
    parse_categories(source_dir)


def parse_categories(source_dir):
    categories_dir = os.path.join(source_dir, settings.CATEGORIES_DIR)
    info('Parsing categories directory', categories_dir)
    for category_dn in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category_dn)
        info('Parsing category directory', category_dir)
        parse_category(category_dir)


def parse_category(category_path):
    """
    Saves category object to database, returns Category object
    """
    category_config = os.path.join(category_path,
                                   settings.CATEGORY_CONFIG_FILE)
    metadata = {}
    if os.path.isfile(category_config):
        info("Loading category config JSON", category_config)
        with open(category_config, 'r') as config_file:
            raw = json.load(config_file)
        for k, v in raw.iteritems():
            metadata[k.lower()] = v
        info("Loaded category metadata", metadata)

    dirname = os.path.split(category_path)[1]
    verbose_name = metadata.pop(
        'verbose_name',
        dirname.title().replace('-', ' ').replace('_', ' ')
    )
    slug = slugify(unicode(metadata.pop('slug', dirname)))
    description = metadata.pop('description', '')
    extras_json = json.dumps(metadata)

    # save category to db
    c = Category.objects.create(
        _dirname=dirname,
        verbose_name=verbose_name,
        slug=slug,
        description=description,
        _extras_json=extras_json,
    )
    info('Created Category object in database', c)
    return c


# def
#     # save pages
#     post_templates = []
#     for fn in os.listdir(category_path):
#         if not fnmatch.fnmatch(fn, settings.POST_TEMPLATES_MATCH):
#             parse_category_page(os.path.join(category_path, fn))
#         else:
#             post_templates.append(os.path.join(category_path, fn))

#     # save posts
#     if settings.POSTS_DIR in os.listdir(category_path):
#         for p_fn in os.listdir(os.path.join(category_path, settings.POSTS_DIR)):
#             p_path = os.path.join(settings.category_path,
#                                   settings.POSTS_DIR,
#                                   p_fn)
#             parse_post(p_path, post_templates)




#     category_path = category_path.rstrip('/')
#     category_dn = os.path.split(category_path)[1]
#     if not os.path.isdir(category_path):
#         msg = """Expected a directory and received [{file}]
#         """.format(file=category_path).strip()
#         raise ValueError(msg)

#     # Get metadata from category-config
#     category_config = os.path.join(category_path,
#                                    settings.CATEGORY_CONFIG_FILENAME)
#     metadata = {}
#     if path.exists(category_config):
#         with open(category_config, 'r') as config_file:
#             raw = json.load(config_file)
#         for k, v in raw.iteritems():
#             metadata[k.lower()] = v

#     verbose_name = metadata.get('verbose_name', category_dn.title())
#     slug = slugify(unicode(category_dn))
#     description = metadata.get('description', '')

#     category = Category(
#         verbose_name=verbose_name,
#         dir_name=category_dn,
#         slug=slug,
#         description=description,
#     )

#     return category


# def parse_post(md_file_path, post_templates):
#     """
#     Return a Post object from a post markdown source file absolute path.

#     Expects Category model to be populated for looking up related Category.

#     Params:
#         - md_file_path is path to post md source file
#         - post_templates is a list of abspaths of post templates
#     """
#     filename = path.splitext(path.split(md_file_path)[1])
#     dirname = path.split(path.dirname(path.dirname(md_file_path)))[1]

#     if filename[1] != '.md':
#         raise Exception("Post source files must be in markdown format.")

#     if Category.objects.all().count() == 0:
#         raise Exception("Populate Categories first so Posts can be related.")

#     # Create post dict with html, get metadata from markdown
#     with open(md_file_path, 'r') as f:
#         post_text = f.read()
#     md = markdown.Markdown(extensions=['markdown.extensions.meta'])
#     html = md.convert(post_text)

#     # Lowercase metadata keys and join the list elements to a single string
#     metadata = {}
#     for k, v in md.Meta.iteritems():
#         metadata[k.lower()] = ''.join(v)

#     author = metadata.get('author', settings.AUTHOR_DEFAULT)
#     date = metadata.get('date', '')
#     title = metadata.get('title', filename[0].title())
#     slug = slugify(unicode(filename[0]))
#     preview = metadata.get('preview', '')

#     published = metadata.get('published')
#     if published:
#         published = True if published.lower() == "true" else False
#     else:
#         published = settings.PUBLISHED_DEFAULT

#     if 'tags' in metadata:
#         tags_list = []
#         for tag in metadata['tags'].split(','):
#             tags_list.append(slugify(unicode(tag)))
#         tags_csv = ','.join(tags_list)
#     else:
#         tags_csv = ''

#     category = Category.objects.get(slug=slugify(unicode(dirname)))

#     post = Post(
#         title=title,
#         slug=slug,
#         author=author,
#         category=category,
#         tags_csv=tags_csv,
#         date=date,
#         published=published,
#         html=html,
#         preview=preview,
#     )

#     return post


# def parse_page(page_path):
#     pass
