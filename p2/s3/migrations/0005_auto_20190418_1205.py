# Generated by Django 2.2 on 2019-04-18 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p2_s3', '0004_auto_20190415_2155'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='s3accesskey',
            unique_together={('access_key', 'secret_key')},
        ),
    ]