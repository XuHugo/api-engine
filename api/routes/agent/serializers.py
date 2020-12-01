from rest_framework import serializers
from api.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class AgentCreateBody(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("name", "type", "urls")
        extra_kwargs = {
            "name": {"required": True},
            "type": {"required": True},
            "urls": {"required": True},
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
