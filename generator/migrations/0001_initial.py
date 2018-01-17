# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-08 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=120)),
                ('content', models.TextField()),
                ('annotations', picklefield.fields.PickledObjectField(editable=False)),
                ('generated', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('originial_url', models.URLField(blank=True)),
                ('original_slug', models.CharField(blank=True, max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.Category')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.ContentType')),
                ('original_document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='generator.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Outlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=50)),
                ('website', models.URLField(blank=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='outlet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.Outlet'),
        ),
    ]