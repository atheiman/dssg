from os import listdir, path
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from dssg.models import Category, Post
from dssg.utils import build_category, build_post


CATEGORIES_DIR = settings.CATEGORIES_DIR
POSTS_DIR_NAME = settings.POSTS_DIR_NAME


class Command(BaseCommand):
    help = 'Populate the database from static site source'

    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Clear database contents before populating'),
        )

    def handle(self, **options):
        if options['delete']:
            Category.objects.all().delete()
            Post.objects.all().delete()
            self.stdout.write('Deleted all Category and Post db records.')

        post_counter = category_counter = 0
        # Loop through category directories
        for category_dn in listdir(CATEGORIES_DIR):
            category_dir = path.join(CATEGORIES_DIR, category_dn)
            posts_dir = path.join(category_dir, POSTS_DIR_NAME)

            # save the category to the db
            category = build_category(category_dir)
            category.save()
            category_counter += 1

            # save all category posts to the db
            for post_file in listdir(posts_dir):
                post = build_post(path.join(posts_dir, post_file))
                post.save()
                post_counter +=1
        self.stdout.write(
            '{c} Categories and {p} Posts created.'.format(
                c=category_counter, p=post_counter)
        )

