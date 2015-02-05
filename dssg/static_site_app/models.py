import os
import json

from django.db import models
from django.utils.text import slugify
from django.conf import settings



class Category(models.Model):
    _dirname = models.CharField(max_length=1023,)
    def _get_source_path(self):
        return os.path.join(settings.SOURCE_DIR,
                            settings.CATEGORIES_DIR,
                            self._dirname,)
    _source_path = property(_get_source_path)

    verbose_name = models.CharField(max_length=1023,
                                    unique=True,)
    slug = models.CharField(max_length=1023,
                            unique=True,)
    description = models.TextField(max_length=1000,
                                   blank=True,)

    def _get_url(self):
        return '/'.join([settings.URL_PREFIX, self.slug,]) + '/'
    url = property(_get_url)

    _extras_json = models.CharField(max_length=1023,
                                    blank=True,)
    def _get_extras(self):
        try:
            return json.loads(self.extras_json)
        except ValueError, TypeError:
            return {}
    extras = property(_get_extras)

    def __unicode__(self):
        return self.verbose_name



class Post(models.Model):
    _category_dirname = models.CharField(max_length=1023,)
    _filename = models.CharField(max_length=1023,
                                 unique=True,)
    def _get_source_path(self):
        return os.path.join(settings.SOURCE_DIR,
                            settings.CATEGORIES_DIR,
                            self._category_dirname,
                            settings.POSTS_DIR,
                            self._filename,)
    _source_path = property(_get_source_path)

    def _get_output_path(self):
        return '/'.join([self.category.slug,
                         self.slug + '.html',])
    _output_path = property(_get_output_path)

    title = models.CharField(max_length=1023,
                             unique=True,)
    slug = models.CharField(max_length=1023,
                            unique=True,)
    author = models.CharField(max_length=1023,
                              blank=True,)
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 related_name='posts',)
    date = models.DateField(blank=True,)
    published = models.BooleanField(default=settings.PUBLISHED_DEFAULT,)
    html = models.TextField()
    preview = models.TextField(max_length=1000,
                               blank=True,)

    def _get_url(self):
        return '/'.join([settings.URL_PREFIX, self._get_output_path(),])
    url = property(_get_url)

    _extras_json = models.CharField(max_length=1023,
                                   blank=True,)
    def _get_extras(self):
        try:
            return json.loads(self.extras_json)
        except ValueError, TypeError:
            return {}
    extras = property(_get_extras)

    def __unicode__(self):
        return self.title
