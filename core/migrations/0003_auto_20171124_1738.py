# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 17:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_enrty'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Enrty',
            new_name='Entry',
        ),
    ]