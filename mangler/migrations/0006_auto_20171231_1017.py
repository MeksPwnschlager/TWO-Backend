# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-31 10:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mangler', '0005_auto_20171231_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mangler.Document'),
        ),
    ]