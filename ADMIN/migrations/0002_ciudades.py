# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-25 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ADMIN', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]