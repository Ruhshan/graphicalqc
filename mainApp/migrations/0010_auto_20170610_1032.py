# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 10:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0009_delete_lab'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.TextField(blank=True, null=True)),
                ('thana', models.CharField(blank=True, max_length=50)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('district', models.CharField(choices=[(b'1', b'DHAKA'), (b'2', b'CHITTAGONG')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Lab')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='lab',
            unique_together=set([('name', 'thana')]),
        ),
    ]