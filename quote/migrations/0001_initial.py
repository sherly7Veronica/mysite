# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-10 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stakeholder', '0002_auto_20181205_0634'),
        ('hubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('for_date', models.DateTimeField()),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('rate_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destname', to='hubs.Hubs')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sourcename', to='hubs.Hubs')),
                ('stakeholder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stakeholder.Stakeholder')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]