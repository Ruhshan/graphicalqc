# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 14:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0025_auto_20170721_0755'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='datapoint',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='datapoint',
            name='lab',
        ),
        migrations.RemoveField(
            model_name='qc',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='qc',
            name='lab',
        ),
        migrations.AlterField(
            model_name='qcdata',
            name='test_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.TestParameters'),
        ),
        migrations.DeleteModel(
            name='DataPoint',
        ),
        migrations.DeleteModel(
            name='QC',
        ),
    ]
