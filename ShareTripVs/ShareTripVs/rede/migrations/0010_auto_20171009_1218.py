# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 15:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rede', '0009_auto_20171009_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viagem',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 9, 12, 18, 23, 847000), verbose_name='Data'),
        ),
    ]
