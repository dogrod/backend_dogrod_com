# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 10:04
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.TaggedPost', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]