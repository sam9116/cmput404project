# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 04:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('authorid1', 'authorid2')]),
        ),
    ]
