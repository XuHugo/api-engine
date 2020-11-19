from rest_framework import serializers
from api.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        #fields = ["id", "name", "agent", "network", "channel", "status", "create_ts"]

