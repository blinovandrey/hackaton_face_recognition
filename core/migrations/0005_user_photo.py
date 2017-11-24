# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 20:02
from __future__ import unicode_literals

from django.db import migrations
import stdimage.models
import stdimage.utils


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_shedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=stdimage.models.StdImageField(null=True, upload_to=stdimage.utils.UploadToClassNameDirUUID(), verbose_name='image'),
        ),
    ]
