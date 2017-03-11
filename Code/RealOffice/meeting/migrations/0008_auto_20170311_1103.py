# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 11:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0007_auto_20170307_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.IntegerField(choices=[(1, 'SCHEDULED'), (2, 'RUNNING'), (3, 'POST_MEETING'), (4, 'FINISHED'), (5, 'CANCELLED')], default=1),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='recipientType',
            field=models.IntegerField(choices=[(1, 'User'), (2, 'Person')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
