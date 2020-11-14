# Generated by Django 3.1.3 on 2020-11-18 15:00

import api.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NetWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('consensus', models.CharField(max_length=128)),
                ('version', models.CharField(max_length=128)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('agent', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=128)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
                ('msp', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('tls', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.channel')),
                ('network', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.network')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('roles', models.CharField(max_length=128)),
                ('attributes', models.CharField(max_length=128)),
                ('revoked', models.CharField(max_length=128)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
                ('msp', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('tls', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('urls', models.URLField()),
                ('status', models.CharField(max_length=128)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
                ('msp', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('tls', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('config_file', models.FileField(max_length=128, upload_to=api.models.upload_to)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organization')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.network'),
        ),
        migrations.CreateModel(
            name='ChainCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('version', models.CharField(max_length=128)),
                ('creator', models.CharField(max_length=128)),
                ('language', models.CharField(max_length=128)),
                ('install_times', models.DateTimeField(auto_now_add=True)),
                ('instantiate_times', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=128)),
                ('channel', models.ManyToManyField(to='api.Channel')),
                ('node', models.ManyToManyField(related_name='node', to='api.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('urls', models.URLField()),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=128)),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization', to='api.organization')),
            ],
        ),
    ]
