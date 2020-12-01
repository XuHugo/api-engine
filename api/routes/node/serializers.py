
from rest_framework import serializers
from api.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class NodeQuery(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("name", "id")
        extra_kwargs = {"name": {"required": False}}


class NodeCreateBody(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("name",)
        extra_kwargs = {"name": {"required": True}}


class NodeIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="ID of Organization")
