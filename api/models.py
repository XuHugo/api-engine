
from django.db import models
import uuid

# Create your models here.

MEDIA_ROOT = "/opt"


def upload_to(instance, filename):
    return '/'.join([MEDIA_ROOT, instance.user_name, filename])


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    agent = models.CharField(max_length=128)
    network = models.ForeignKey("NetWork", null=True, on_delete=models.SET_NULL)
    channel = models.ForeignKey("Channel", null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=128)
    create_ts = models.DateTimeField(auto_now_add=True)
    msp = models.FileField(upload_to=upload_to, max_length=128)
    tls = models.FileField(upload_to=upload_to, max_length=128)


class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    urls = models.URLField(max_length=200)
    organization = models.OneToOneField("Organization", null=True, on_delete=models.SET_NULL, related_name="organization")
    create_ts = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=128)


class NetWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    consensus = models.CharField(max_length=128)
    version = models.CharField(max_length=128)
    create_ts = models.DateTimeField(auto_now_add=True)


class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    urls = models.URLField(max_length=200)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    create_ts = models.DateTimeField(auto_now_add=True)
    msp = models.FileField(upload_to=upload_to, max_length=128)
    tls = models.FileField(upload_to=upload_to, max_length=128)
    config_file = models.FileField(upload_to=upload_to, max_length=128)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    roles = models.CharField(max_length=128)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    attributes = models.CharField(max_length=128)
    revoked = models.CharField(max_length=128)
    create_ts = models.DateTimeField(auto_now_add=True)
    msp = models.FileField(upload_to=upload_to, max_length=128)
    tls = models.FileField(upload_to=upload_to, max_length=128)


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    network = models.ForeignKey("NetWork", on_delete=models.CASCADE)
    create_ts = models.DateTimeField(auto_now_add=True)


class ChainCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    version = models.CharField(max_length=128)
    creator = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    channel = models.ManyToManyField("Channel")
    install_times = models.DateTimeField(auto_now_add=True)
    instantiate_times = models.DateTimeField(auto_now_add=True)
    node = models.ManyToManyField("Node",  related_name='node')
    status = models.CharField(max_length=128)

