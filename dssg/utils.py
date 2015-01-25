"""
Utilities for dssg.
"""

from os import path, listdir, mkdir
import shutil
import json

import markdown
from django.utils.text import slugify
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from .models import Post, Category


CATEGORIES_DIR = settings.CATEGORIES_DIR
POSTS_DIR_NAME = settings.POSTS_DIR_NAME
OUTPUT_DIR = settings.OUTPUT_DIR
OUTPUT_BACKUP_DIR = settings.OUTPUT_BACKUP_DIR
CATEGORY_CONFIG_FILENAME = settings.CATEGORY_CONFIG_FILENAME
POST_TEMPLATE_NAME = settings.POST_TEMPLATE_NAME
STATIC_DIR_NAME = settings.STATIC_DIR_NAME
STATIC_DIR = settings.STATIC_DIR
PAGES_DIR = settings.PAGES_DIR


def build_category(category_path):
    """
    Return a Category object from a category directory absolute path.
    """
    category_path = category_path.rstrip('/')
    category_dn = path.split(category_path)[1]
    if not path.isdir(category_path):
        msg = """Expected a directory and received [{file}]
        """.format(file=category_path).strip()
        raise ValueError(msg)

    # Get metadata from category-config
    category_config = path.join(category_path,
                                   settings.CATEGORY_CONFIG_FILENAME)
    metadata = {}
    if path.exists(category_config):
        with open(category_config, 'r') as config_file:
            raw = json.load(config_file)
        for k, v in raw.iteritems():
            metadata[k.lower()] = v

    verbose_name = metadata.get('verbose_name', category_dn.title())
    slug = slugify(unicode(category_dn))
    description = metadata.get('description', '')

    category = Category(
        verbose_name=verbose_name,
        slug=slug,
        description=description,
    )

    return category



def build_post(md_file_path):
    """
    Return a Post object from a post markdown source file absolute path.

    Expects Category model to be populated for looking up related Category.
    """
    filename = path.splitext(path.split(md_file_path)[1])
    dirname = path.split(path.dirname(path.dirname(md_file_path)))[1]

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
    slug = slugify(unicode(filename[0]))
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

    category = Category.objects.get(slug=slugify(unicode(dirname)))

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



def generate_output():
    """
    Build output at OUTPUT_DIR and return dictionary describing generation:

    {
        'pages': int,
        'categories': int,
        'category_pages': int,
        'posts': int,
    }

    Expects database to be populated, and and empty output dir to exist.
    """
    posts_counter = category_pages_counter = categories_counter = pages_counter = 0

    # create one-off pages at /page-name.html
    for page_name in listdir(PAGES_DIR):
        if page_name == CATEGORY_CONFIG_FILENAME:
            continue
        template = get_template(path.join(path.split(PAGES_DIR)[1],page_name))
        context = Context({
            'categories': Category.objects.all(),
            'posts': Post.objects.all(),
        })
        html = template.render(context)

        with open(path.join(OUTPUT_DIR, page_name), 'w') as f:
            f.write(html)
        pages_counter += 1

    # copy static dir to output dir
    shutil.copytree(STATIC_DIR, path.join(OUTPUT_DIR, STATIC_DIR_NAME))

    # place categories in output
    for c_dn in listdir(CATEGORIES_DIR):
        c_dir = path.join(CATEGORIES_DIR, c_dn)
        c_files = listdir(c_dir)
        c = Category.objects.get(slug=slugify(unicode(c_dn)))
        posts = Post.objects.filter(category=c)

        # make empty category output dir
        c_out_dir = path.join(OUTPUT_DIR, c.slug)
        mkdir(c_out_dir)

        # Place category pages in category output dir
        c_page_context = Context({'posts': posts, 'category': c,})
        for f in c_files:
            if f not in [POSTS_DIR_NAME, POST_TEMPLATE_NAME]:
                t = get_template(path.join(c_dn, f))
                html = t.render(c_page_context)
                with open(path.join(OUTPUT_DIR, c.slug, f), 'w') as f:
                    f.write(html)
                category_pages_counter += 1

        # Place category posts in output dir
        post_t = get_template(path.join(c_dn, POST_TEMPLATE_NAME))
        for p in posts:
            html = post_t.render(Context({'post': p, 'category': c}))
            with open(path.join(OUTPUT_DIR, c.slug, p.slug) + '.html', 'w') as f:
                f.write(html)
            posts_counter += 1

        categories_counter += 1

    return {
        'pages': pages_counter,
        'categories': categories_counter,
        'category_pages': category_pages_counter,
        'posts': posts_counter,
    }
