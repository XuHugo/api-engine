from rest_framework import serializers
from api.models import Agent
from api.routes.organization.serializers import (
    OrganizationSerializer,
    OrganizationCreateBody,
    OrganizationIDSerializer,
    OrganizationQuery,
)


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class AgentCreateBody(serializers.ModelSerializer):
    organization = OrganizationQuery()

    class Meta:
        model = Agent
        fields = ("name", "type", "urls", "organization")
        extra_kwargs = {
            "name": {"required": True},
            "type": {"required": True},
            "urls": {"required": True},
            "organization": {"required": True},
        }


class AgentQuery(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("name", "id", "type", "organization")
        extra_kwargs = {
            "id": {"required": False},
            "name": {"required": True},
            "type": {"required": True},
            "organization": {"required": False},
        }


class AgentIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="ID of Organization")
