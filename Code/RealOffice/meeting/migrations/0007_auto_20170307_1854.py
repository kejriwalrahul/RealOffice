# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0006_auto_20170307_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='orderDetails',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]