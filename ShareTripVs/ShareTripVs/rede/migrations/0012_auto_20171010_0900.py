# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rede', '0011_auto_20171010_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='viagem',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
    ]