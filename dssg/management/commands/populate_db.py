from optparse import make_option

from django.core.management.base import NoArgsCommand

from dssg.models import Category, Post

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

        # actually populate the db
