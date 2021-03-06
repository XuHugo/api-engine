# Generated by Django 3.1.3 on 2020-12-11 00:30

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_organization_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='organizations',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=128), default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='node',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.organization'),
        ),
    ]
