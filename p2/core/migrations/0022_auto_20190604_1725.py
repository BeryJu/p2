# Generated by Django 2.2.1 on 2019-06-04 17:25

from django.db import migrations, models

import p2.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('p2_core', '0021_auto_20190517_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blob',
            name='path',
            field=models.TextField(validators=[p2.core.validators.validate_blob_path]),
        ),
        migrations.AlterField(
            model_name='component',
            name='controller_path',
            field=models.TextField(choices=[('p2.components.image.controller.ImageController', 'ImageController'), ('p2.components.quota.controller.QuotaController', 'QuotaController'), ('p2.components.public_access.controller.PublicAccessController', 'PublicAccessController'), ('p2.components.replication.controller.ReplicationController', 'ReplicationController')]),
        ),
        migrations.AlterField(
            model_name='storage',
            name='controller_path',
            field=models.TextField(choices=[('p2.core.storages.null.NullStorageController', 'NullStorageController'), ('p2.storage.local.controller.LocalStorageController', 'LocalStorageController'), ('p2.storage.s3.controller.S3StorageController', 'S3StorageController')]),
        ),
    ]
