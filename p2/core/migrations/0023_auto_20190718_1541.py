# Generated by Django 2.2.3 on 2019-07-18 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2_core', '0022_auto_20190604_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='controller_path',
            field=models.TextField(choices=[('p2.components.image.controller.ImageController', 'ImageController'), ('p2.components.quota.controller.QuotaController', 'QuotaController'), ('p2.components.public_access.controller.PublicAccessController', 'PublicAccessController'), ('p2.components.replication.controller.ReplicationController', 'ReplicationController'), ('p2.components.expire.controller.ExpiryController', 'ExpiryController')]),
        ),
    ]