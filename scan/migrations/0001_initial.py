# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-19 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScanFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('folderName', models.CharField(max_length=200)),
                ('fileCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ScanJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
