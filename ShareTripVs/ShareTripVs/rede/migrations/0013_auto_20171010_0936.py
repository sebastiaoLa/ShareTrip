# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rede', '0012_auto_20171010_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cpf',
            field=models.CharField(max_length=14, unique=True, verbose_name='cpf'),
        ),
    ]
