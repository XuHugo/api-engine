

from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import Organization
from api.lib.pki import CryptoGen, CryptoConfig
from django.core.exceptions import ObjectDoesNotExist
from api.routes.organization.serializers import (
    OrganizationSerializer,
    OrganizationCreateBody,
    OrganizationIDSerializer,
    OrganizationQuery,
)


class OrganizationViewSet(viewsets.ViewSet):

    def list(self, request):

        queryset = Organization.objects.all()
        serializer = OrganizationSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        serializer = OrganizationCreateBody(data=request.data)
        if serializer.is_valid(raise_exception=True):
            org_name = serializer.validated_data.get("name")
            org_type = serializer.validated_data.get("type")
            #org_hosts = serializer.validated_data.get("hosts")
            try:
                Organization.objects.get(name=org_name)
            except ObjectDoesNotExist:
                pass

            org = {"ca": {
                "country": "china",
                "province": "beijing",
                "locality": "changping"
            },
                "type": org_type,
                "name": org_name.split(".")[0].capitalize(),
                "domain": org_name,
                "enableNodeOUs": True,
                "Specs": ["zoo"]
            }
            cryptoconfig = CryptoConfig(org=org_name)
            cryptoconfig.create(org)

            cryptogen = CryptoGen()
            cryptogen.generate(org_name=org_name)

            organization = Organization(name=org_name)
            organization.save()

            response = OrganizationIDSerializer(data=organization.__dict__)
            if response.is_valid(raise_exception=True):
                return Response(
                    response.validated_data, status=status.HTTP_201_CREATED
                )

    def destroy(self, request, pk=None):
        pass

    def retrieve(self, request, pk=None):
        queryset = Organization.Objects.all()
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

