# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-22 14:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0028_testparameter_lab'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_number', models.CharField(max_length=20)),
                ('control_level', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=10)),
                ('control_data', models.IntegerField()),
                ('remarks', models.CharField(max_length=50)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.Lab')),
                ('test_parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.TestParameter')),
            ],
        ),
        migrations.RemoveField(
            model_name='qcdata',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='qcdata',
            name='lab',
        ),
        migrations.RemoveField(
            model_name='qcdata',
            name='test_name',
        ),
        migrations.DeleteModel(
            name='QCData',
        ),
    ]
