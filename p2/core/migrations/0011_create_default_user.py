# Generated by Django 2.2 on 2019-04-24 11:54

from django.db import migrations


def create_default_user(apps, schema_editor):
    from django.contrib.auth.models import User
    # Ignore Anonymous User
    if len(User.objects.all()) < 2:
        User.objects.create_superuser(
            username='admin',
            email='admin@p2.local',
            password='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('p2_core', '0010_blob_prefix'),
    ]

    operations = [
        migrations.RunPython(create_default_user)
    ]