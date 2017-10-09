# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 14:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rede', '0007_auto_20171009_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
            },
        ),
        migrations.AlterField(
            model_name='viagem',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 9, 11, 45, 45, 33000), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='viagem',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Empresa', to='rede.Empresa'),
        ),
    ]