from rest_framework import serializers
from api.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        #fields = ["id", "name", "agent", "network", "channel", "status", "create_ts"]


class OrganizationQuery(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "id")
        extra_kwargs = {"name": {"required": False}}


class OrganizationCreateBody(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "type")
        extra_kwargs = {"name": {"required": True}, "type": {"required": True}}


class OrganizationIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="ID of Organization")
