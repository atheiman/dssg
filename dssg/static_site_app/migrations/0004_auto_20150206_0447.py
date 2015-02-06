# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('static_site_app', '0003_auto_20150206_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=models.TextField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
