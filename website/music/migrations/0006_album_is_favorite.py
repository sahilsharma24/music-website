# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-13 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20170612_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
