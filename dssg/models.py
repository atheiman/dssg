from django.db import models
from django.utils.text import slugify
from django.conf import settings

from .checks import settings_check, filesystem_check

class Category(models.Model):
    verbose_name = models.CharField(max_length=100,
                            unique=True,)
    slug = models.CharField(max_length=100,
                            unique=True,)
    description = models.TextField(max_length=500,
                                   blank=True,)

    def _get_url(self):
        return '/'.join([settings.URL_PREFIX,
                         self.slug,])
    url = property(_get_url)

    def __unicode__(self):
        return self.verbose_name



class Post(models.Model):
    title = models.CharField(max_length=250,
                             unique=True,)
    slug = models.CharField(max_length=250,
                            unique=True,)
    author = models.CharField(max_length=250,
                              blank=True,)
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 related_name='posts')
    tags_csv = models.TextField(blank=True,)
    date = models.CharField(max_length=100,
                            blank=True,)
    published = models.BooleanField(default=settings.PUBLISHED_DEFAULT,)
    html = models.TextField()
    preview = models.TextField(max_length=500,
                               blank=True,)

    def _get_url(self):
        return '/'.join([settings.URL_PREFIX,
                         self.category.slug,
                         self.slug + '.html',])
    url = property(_get_url)

    def __unicode__(self):
        return self.title
