import shutil
from os import listdir, path, mkdir

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.db import OperationalError

from dssg.models import Category, Post
from dssg.utils import build_category, build_post


CATEGORIES_DIR = settings.CATEGORIES_DIR
POSTS_DIR_NAME = settings.POSTS_DIR_NAME
OUTPUT_DIR = settings.OUTPUT_DIR
OUTPUT_BACKUP_DIR = settings.OUTPUT_BACKUP_DIR
CATEGORY_CONFIG_FILENAME = settings.CATEGORY_CONFIG_FILENAME
POST_TEMPLATE_NAME = settings.POST_TEMPLATE_NAME


class Command(NoArgsCommand):
    help = 'Generate static site output from db'

    def handle_noargs(self, **options):
        try:
            missing_models = []
            if not Category.objects.all():
                missing_models.append('Category')
            if not Post.objects.all():
                missing_models.append('Post')
            if missing_models:
                self.stdout.write(
                    "No %s db records found, have you run `populate_db`? Exiting." %
                    ' or '.join(missing_models)
                )
                return
        except OperationalError:
            self.stdout.write(
                "Database OperationalError, have you run `migrate`? Exiting."
            )

        # replace output-backup, create empty output
        shutil.rmtree(OUTPUT_BACKUP_DIR, ignore_errors=True)
        if path.isdir(OUTPUT_DIR):
            self.stdout.write('Moving existing output dir to output backup.')
            shutil.move(OUTPUT_DIR, OUTPUT_BACKUP_DIR)
        mkdir(OUTPUT_DIR)

        # Loop through category directories
        for c_dn in listdir(CATEGORIES_DIR):
            c_dir = path.join(CATEGORIES_DIR, c_dn)
            c_files = listdir(c_dir)
            c_page_templates = []
            for f in c_files:
                if f not in [POSTS_DIR_NAME, POST_TEMPLATE_NAME]
                c_page_templates.append(get_template(path.join(c_dn, f)))

            c = Category.objects.get(name__iexact=dirname)
            posts = Post.objects.filter(category=c)

            # make empty category output dir
            c_out_dir = path.join(OUTPUT_DIR, c.slug)
            mkdir(c_out_dir)

            # place category pages in category output dir



            # create one-off pages at /page-name.html
            for page_name in listdir(PAGES_DIR):
                template = env.get_template(page_name)
                template_str = template.render(
                    categories=db['categories'],
                    posts=db['posts'],
                )

                with open(path.join(OUTPUT_DIR, page_name), 'w') as out_file:
                    out_file.write(template_str)


            # create category pages at /category-slug/index.html
            # create post pages at /category-slug/post-slug.html
            # create json from posts list at /posts.json


        self.stdout.write(
            """Output dir generated with {c} categories, {po} posts, and {pa} pages.
            """.format(c=category_counter, po=post_counter, pa=page_counter).strip()
        )

