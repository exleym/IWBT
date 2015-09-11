# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gauge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usgs_id', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='GaugeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('flow_level', models.FloatField()),
                ('gauge_level', models.FloatField()),
                ('gauge_id', models.ForeignKey(to='paddlelog.Gauge')),
            ],
        ),
        migrations.CreateModel(
            name='River',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('river_name', models.CharField(max_length=64)),
                ('difficulty', models.CharField(max_length=16)),
                ('max_diff', models.IntegerField()),
                ('gauge_id', models.ForeignKey(to='paddlelog.Gauge')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateField()),
                ('paddle_date', models.DateField()),
                ('flow', models.FloatField()),
                ('level', models.FloatField()),
                ('river_id', models.ForeignKey(to='paddlelog.River')),
            ],
        ),
        migrations.CreateModel(
            name='TripKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TripVarData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=128)),
                ('key', models.ForeignKey(to='paddlelog.TripKey')),
                ('trip_id', models.ForeignKey(to='paddlelog.Trip')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=32)),
                ('create_date', models.DateField()),
                ('pw_salt', models.CharField(max_length=16)),
                ('pw_hashed', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='user_id',
            field=models.ForeignKey(to='paddlelog.User'),
        ),
    ]
