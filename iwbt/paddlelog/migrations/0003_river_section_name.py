# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paddlelog', '0002_trip_swim_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='river',
            name='section_name',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
    ]
