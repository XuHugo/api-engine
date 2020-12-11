from rest_framework import serializers
from api.models import NetWork


class NetWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetWork
        fields = '__all__'


class NetWorkQuery(serializers.ModelSerializer):
    class Meta:
        model = NetWork
        fields = ("name", "id")
        extra_kwargs = {"name": {"required": False}}


class NetWorkCreateBody(serializers.ModelSerializer):
    class Meta:
        model = NetWork
        fields = ("name", "consensus", "organizations")
        extra_kwargs = {"name": {"required": True},
                        "consensus": {"required": True},
                        "organizations":{"required": True}}


class NetWorkIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="ID of NetWork")
