# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 11:14
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rede', '0002_auto_20171008_0806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('de', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Solicitante', to=settings.AUTH_USER_MODEL)),
                ('para', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Solicitado', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['data'],
                'verbose_name': 'solicitacao',
                'verbose_name_plural': 'solicitacoes',
            },
        ),
        migrations.AlterField(
            model_name='viagem',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 8, 14, 48, 800000), verbose_name='Data'),
        ),
    ]
