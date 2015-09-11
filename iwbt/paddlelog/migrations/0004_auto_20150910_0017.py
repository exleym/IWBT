# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paddlelog', '0003_river_section_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pw_hashed',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pw_salt',
        ),
    ]
