"""
Utilities for dssg.
"""

import os
import json

import markdown
from django.utils.text import slugify
from django.conf import settings

from .models import Post, Category



def build_category(category_path):
    """
    Return a Category object from a category directory absolute path.
    """
    category_path = category_path.rstrip('/')
    category_dn = os.path.split(category_path)[1]
    if not os.path.isdir(category_path):
        msg = """Expected a directory and received [{file}]
        """.format(file=category_path).strip()
        raise ValueError(msg)

    # Get metadata from category-config
    category_config = os.path.join(category_path,
                                   settings.CATEGORY_CONFIG_FILENAME)
    metadata = {}
    if os.path.exists(category_config):
        with open(category_config, 'r') as config_file:
            raw = json.load(config_file)
        for k, v in raw.iteritems():
            metadata[k.lower()] = v

    name = metadata.get('name', unicode(category_dn.title()))
    slug = slugify(unicode(metadata.get('slug', category_dn)))
    description = metadata.get('description', '')

    category = Category(
        name=name,
        slug=slug,
        description=description,
    )

    return category



def build_post(md_file_path):
    """
    Return a Post object from a post markdown source file absolute path.

    Expects Category model to be populated for looking up related Category.
    """
    filename = os.path.splitext(os.path.split(md_file_path)[1])
    dirname = os.path.split(os.path.dirname(os.path.dirname(md_file_path)))[1]

    if filename[1] != '.md':
        raise Exception("Post source files must be in markdown format.")

    if Category.objects.all().count() == 0:
        raise Exception("Populate Categories first so Posts can be related.")

    # Create post dict with html, get metadata from markdown
    with open(md_file_path, 'r') as f:
        post_text = f.read()
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(post_text)

    # Lowercase metadata keys and join the list elements to a single string
    metadata = {}
    for k, v in md.Meta.iteritems():
        metadata[k.lower()] = ''.join(v)

    author = metadata.get('author', settings.AUTHOR_DEFAULT)
    date = metadata.get('date', '')
    title = metadata.get('title', filename[0].title())
    slug = slugify(unicode(metadata.get('slug', filename[0])))
    preview = metadata.get('preview', '')

    published = metadata.get('published')
    if published:
        published = True if published.lower() == "true" else False
    else:
        published = settings.PUBLISHED_DEFAULT

    if 'tags' in metadata:
        tags_list = []
        for tag in metadata['tags'].split(','):
            tags_list.append(slugify(unicode(tag)))
        tags_csv = ','.join(tags_list)
    else:
        tags_csv = ''

    category = Category.objects.get(name__iexact=dirname)

    post = Post(
        title=title,
        slug=slug,
        author=author,
        category=category,
        tags_csv=tags_csv,
        date=date,
        published=published,
        html=html,
        preview=preview,
    )

    return post
