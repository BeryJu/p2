# Generated by Django 2.2.4 on 2019-08-29 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2_core', '0023_auto_20190718_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volume',
            name='name',
            field=models.SlugField(max_length=63, unique=True),
        ),
    ]
