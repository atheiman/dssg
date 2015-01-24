from django.db import models
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,)
    slug = models.SlugField(max_length=100,
                            unique=True,)
    description = models.TextField(max_length=500,
                                   blank=True,)

    def _get_url(self):
        return '/'.join([URL_PREFIX,
                        self.slug,])
    url = property(_get_url)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=250,
                             unique=True,)
    slug = models.SlugField(max_length=250,
                            unique=True,)
    author = models.CharField(max_length=250,
                              blank=True,)
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,)
    tags_csv = models.TextField(blank=True,)
    date = models.CharField(blank=True,
                            null=True,)
    published = models.BooleanField()
    html = models.TextField()
    preview = models.TextField(max_length=500,
                               blank=True,)

    def _get_url(self):
        return '/'.join([URL_PREFIX,
                        self.category.slug,
                        self.slug + '.html',])
    url = property(_get_url)

    def save(self, *args, **kwargs):
        # create slug based on title of post
        if not self.slug:
            self.slug = slugify(unicode(self.title))

        # save to db
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
