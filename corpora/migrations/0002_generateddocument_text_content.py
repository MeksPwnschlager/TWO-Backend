# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-22 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='generateddocument',
            name='text_content',
            field=models.TextField(default=''),
        ),
    ]
