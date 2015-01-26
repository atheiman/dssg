import shutil
from os import path, mkdir, listdir, remove, unlink

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.db import OperationalError

from dssg.models import Category, Post
from dssg.utils import generate_output


OUTPUT_DIR = settings.OUTPUT_DIR
OUTPUT_BACKUP_DIR = settings.OUTPUT_BACKUP_DIR


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

        # empty the backup dir
        if not path.isdir(OUTPUT_DIR):
            mkdir(OUTPUT_DIR)
        for fn in listdir(OUTPUT_DIR):
            f = path.join(OUTPUT_DIR, fn)
            if path.isdir(f):
                shutil.rmtree(f)
            elif path.islink:
                unlink(f)
            elif path.isfile(f):
                remove(f)

        summary = generate_output()

        self.stdout.write(
            """Output generated in {dir}:\n{summary}
            """.format(dir=OUTPUT_DIR, summary=str(summary)).strip()
        )

