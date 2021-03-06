# Generated by Django 2.2 on 2019-04-08 20:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2_log', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DatabaseLogAdaptor',
        ),
        migrations.CreateModel(
            name='DatabaseLogAdaptor',
            fields=[
                ('logadaptor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='p2_log.LogAdaptor')),
            ],
            options={
                'abstract': False,
            },
            bases=('p2_log.logadaptor',),
        ),
        migrations.AlterField(
            model_name='Record',
            name='adaptor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='p2_log.LogAdaptor'),
        ),
    ]
