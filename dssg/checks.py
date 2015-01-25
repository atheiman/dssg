from os import listdir, path

from django.core.checks import register, Error
from django.conf import settings


CATEGORIES_DIR = settings.CATEGORIES_DIR
POSTS_DIR_NAME = settings.POSTS_DIR_NAME


@register('settings')
def settings_check(app_configs, **kwargs):
    required_attrs = [
        'CATEGORIES_DIR',
        'CATEGORY_CONFIG_FILENAME',
        'CATEGORY_POST_TEMPLATE_NAME',
        'POSTS_DIR_NAME',
        'PAGES_DIR',
        'INCLUDES_DIR',
        'STATIC_DIR_NAME',
        'STATIC_DIR',
        'OUTPUT_DIR',
        'AUTHOR_DEFAULT',
        'PUBLISHED_DEFAULT',
        'URL_PREFIX',
        'STATIC_URL',
        'TEMPLATE_DIRS',
    ]
    errors = []
    for attr in required_attrs:
        if not hasattr(settings, attr):
            errors.append(Error(
                "Missing required setting '%s'" % attr,
                hint=None,
                obj=settings,
                id='dssg.E001',
            ))
    return errors


@register('filesystem')
def filesystem_check(app_configs, **kwargs):
    errors = []
    for category_dn in listdir(CATEGORIES_DIR):
        try:
            for post_filename in listdir(path.join(CATEGORIES_DIR,
                                                   category_dn,
                                                   POSTS_DIR_NAME)):
                if path.splitext(post_filename)[1] != '.md':
                    hint = """Only Markdown post source files should exist in {dir}
                    """.format(dir=path.join(CATEGORIES_DIR,
                                             category_dn,
                                             POSTS_DIR_NAME))
                    errors.append(Error(
                        "Non-markdown post source file found in posts directory",
                        hint=hint.strip(),
                        obj=post_filename,
                        id='dssg.E003',
                    ))

        except OSError:   # non dir in categories/
            hint = """Only category directories should exist in {dir}
            """.format(dir=CATEGORIES_DIR)
            errors.append(Error(
                "Non-directory found in categories directory",
                hint=hint.strip(),
                obj=category_dn,
                id='dssg.E002',
            ))

    return errors
