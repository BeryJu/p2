# Generated by Django 2.2.1 on 2019-05-09 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p2_serve', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverule',
            name='default',
        ),
    ]
