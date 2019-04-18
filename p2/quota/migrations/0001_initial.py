# Generated by Django 2.2 on 2019-04-18 12:05

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('p2_core', '0008_auto_20190403_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('threshold', models.IntegerField()),
                ('action', models.TextField(choices=[('nothing', 'Do nothing, just show warning in UI.'), ('block', 'Prevent further uploads to this volume.'), ('e-mail', 'Send E-Mail to uploader and admin.')], default='nothing')),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='p2_core.Volume')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
