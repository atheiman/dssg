"""
Parsers for reading in a source directory and saving objects to a database.
"""

import os
import shutil
import json
import fnmatch

import markdown
from django.utils.text import slugify
from django.utils.dateparse import parse_date
from django.template import Context
from django.template.loader import get_template
from django.conf import settings

from dssg.static_site_app.models import Post, Category
from dssg.writers import write_category_page, write_post
from dssg.utils.simplog import error, warn, info
from dssg.utils.text import string_to_boolean


def parse_source_dir(source_dir):
    parse_categories(source_dir)
    parse_pages(source_dir)


def parse_categories(source_dir):
    categories_dir = os.path.join(source_dir, settings.CATEGORIES_DIR)
    info('Parsing categories directory', categories_dir)
    for category_dn in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category_dn)
        info('Parsing category directory', category_dir)
        c = parse_category(category_dir)

    for category_dn in os.listdir(categories_dir):
        category_dir = os.path.join(categories_dir, category_dn)
        c = Category.objects.get(_dirname=category_dn)

        # save all posts to db
        if settings.POSTS_DIR in os.listdir(category_dir):
            info('Saving posts to db')
            posts_dir = os.path.join(category_dir, settings.POSTS_DIR)
            for p_fn in os.listdir(posts_dir):
                p_path = os.path.join(posts_dir, p_fn)
                info('Parsing post', p_path)
                p = parse_post(p_path)

        # write pages
        post_templates = []
        for fn in os.listdir(category_dir):
            if fn == settings.POSTS_DIR:
                continue
            if not fnmatch.fnmatch(fn, settings.POST_TEMPLATES_MATCH):
                p = parse_category_page(os.path.join(category_dir, fn), c)
                write_category_page(p, c)
            else:
                post_templates.append(os.path.join(category_dn, fn))

        # write posts with post templates
        if post_templates:
            info('Rendering posts with post templates', post_templates)
            posts_dir = os.path.join(category_dir, settings.POSTS_DIR)
            for p in c.posts.all():
                post_files = render_post(p, post_templates)
                write_post(p, post_files)


def parse_category(category_path):
    """
    Saves Category object to database, returns Category object
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


def parse_category_page(page_path, category):
    """
    Returns a page_dict to be used by writers.write_category_page().
    """
    filename = os.path.split(page_path)[1]
    template = get_template(os.path.join(category._dirname, filename))
    context = Context({
        'c': category,
        'posts': category.posts.all(),
        'categories': Category.objects.all(),
        'URL_PREFIX': settings.URL_PREFIX,
    })
    source = template.render(context)
    return {'filename': filename, 'source': source}


def parse_post(p_path):
    """
    Saves Post object to database. Returns Post object.

    Returns None and does not save a Post if Post.published should be False.
    """
    filename = os.path.split(p_path)[1]
    with open(p_path, 'r') as f:
        post_text = f.read()
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(post_text)

    metadata = {}
    for k, v in md.Meta.iteritems():
        if not v:
            continue
        if len(v) == 1:
            metadata[k] = v[0]
        if len(v) > 1:
            warn('Post markdown source metadata value spans multiple lines.',
                 p_path)
            metadata[k] = '\n'.join(v)

    try:
        published = string_to_boolean(metadata.pop('published', None))
    except ValueError:
        published = settings.PUBLISHED_DEFAULT
    if not published:
        return None

    title = metadata.pop(
        'title',
        filename.title().replace('-', ' ').replace('_', ' ')
    )
    slug = slugify(unicode(metadata.pop('slug', filename)))
    author = metadata.pop('author', settings.AUTHOR_DEFAULT)
    category = Category.objects.get(
        _dirname=os.path.split(os.path.dirname(os.path.dirname(p_path)))[1]
    )
    date = parse_date(metadata.pop('date', None))
    preview = metadata.pop('preview', None)
    extras_json = json.dumps(metadata)

    p = Post.objects.create(
        _filename=filename,
        title=title,
        slug=slug,
        author=author,
        category=category,
        date=date,
        published=published,
        html=html,
        preview=preview,
        _extras_json=extras_json,
    )
    return p


def render_post(post, post_templates):
    """
    Returns a list of post file dicts to be written to output.

    post_templates should be a list of template paths for rendering the post.
    Each template path should be in the format:

        'category_dirname/template.html'
    """
    post_files = []
    for t_path in post_templates:
        info('Rendering post with template', [post, t_path])
        template = get_template(t_path)
        context = Context({
            'p': post,
            'c': post.category,
            'categories': Category.objects.all(),
            'URL_PREFIX': settings.URL_PREFIX,
        })
        post_files.append({
            'source': template.render(context),
            'filename': post.slug + os.path.splitext(t_path)[1],
        })
    return post_files


def parse_pages(source_dir):
    return



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
