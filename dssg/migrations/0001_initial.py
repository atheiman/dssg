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
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField(max_length=500, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250)),
                ('author', models.CharField(max_length=250, blank=True)),
                ('tags_csv', models.TextField(blank=True)),
                ('date', models.CharField(max_length=100, blank=True)),
                ('published', models.BooleanField(default=True)),
                ('html', models.TextField()),
                ('preview', models.TextField(max_length=500, blank=True)),
                ('category', models.ForeignKey(blank=True, to='dssg.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
