
from rest_framework import serializers
from api.models import Node
from api.routes.organization.serializers import (
    OrganizationSerializer,
    OrganizationCreateBody,
    OrganizationIDSerializer,
    OrganizationQuery,
)


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
    organization = OrganizationQuery()

    class Meta:
        model = Node
        fields = ("name", "type", "organization", "urls")
        extra_kwargs = {"name": {"required": True},
                        "type": {"required": True},
                        "organization": {"required": True}}


class NodeIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="ID of Organization")
