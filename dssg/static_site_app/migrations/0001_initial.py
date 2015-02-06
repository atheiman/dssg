# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_dirname', models.CharField(max_length=1023)),
                ('verbose_name', models.CharField(unique=True, max_length=1023)),
                ('slug', models.CharField(unique=True, max_length=1023)),
                ('description', models.TextField(max_length=1000, blank=True)),
                ('_extras_json', models.CharField(max_length=1023, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_category_dirname', models.CharField(max_length=1023)),
                ('_filename', models.CharField(unique=True, max_length=1023)),
                ('title', models.CharField(unique=True, max_length=1023)),
                ('slug', models.CharField(unique=True, max_length=1023)),
                ('author', models.CharField(max_length=1023, blank=True)),
                ('date', models.DateField(blank=True)),
                ('published', models.BooleanField(default=True)),
                ('html', models.TextField()),
                ('preview', models.TextField(max_length=1000, blank=True)),
                ('_extras_json', models.CharField(max_length=1023, blank=True)),
                ('category', models.ForeignKey(related_name='posts', blank=True, to='static_site_app.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
