from os import listdir, path
from optparse import make_option

from django.core.management.base import NoArgsCommand

from dssg.models import Category, Post
from dssg.utils import build_category, build_post

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
            self.stdout.write('Deleted all Category and Post db records')

        for category_dn in os.listdir(CATEGORIES_DIR):
            category_dir = os.path.join(CATEGORIES_DIR, category_dn)
            posts_dir = os.path.join(category_dir, POSTS_DIR_NAME)
