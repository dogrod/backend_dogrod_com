# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 10:22
from __future__ import unicode_literals

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UpyunMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, verbose_name='file_name')),
                ('url', models.FileField(storage=media.models.UpYunStorage(), upload_to='media', verbose_name='URL')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
