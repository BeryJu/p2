# Generated by Django 2.2 on 2019-04-30 12:08

import uuid

import django.contrib.postgres.fields.hstore
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2_core', '0012_auto_20190430_0924'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blob',
            options={'verbose_name': 'Blob', 'verbose_name_plural': 'Blobs'},
        ),
        migrations.AlterModelOptions(
            name='storage',
            options={'permissions': (('use_storage', 'Can use storage'),), 'verbose_name': 'Storage', 'verbose_name_plural': 'Storages'},
        ),
        migrations.AlterModelOptions(
            name='volume',
            options={'permissions': (('list_contents', 'List contents'), ('use_volume', 'Use Volume')), 'verbose_name': 'Volume', 'verbose_name_plural': 'Volumes'},
        ),
        migrations.RenameField(
            model_name='storage',
            old_name='controller',
            new_name='controller_path'
        ),
        migrations.AlterField(
            model_name='storage',
            name='controller_path',
            field=models.TextField(choices=[('p2.core.storages.null.NullStorageController', 'NullStorageController'), ('p2.storage.local.controller.LocalStorageController', 'LocalStorageController')], default=''),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('tags', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict)),
                ('controller_path', models.TextField(choices=[('p2.components.image.controller.ImageController', 'ImageController'), ('p2.components.quota.controller.QuotaController', 'QuotaController')])),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='p2_core.Volume')),
            ],
            options={
                'verbose_name': 'Component',
                'verbose_name_plural': 'Components',
                'unique_together': {('volume', 'controller_path')},
            },
        ),
    ]
