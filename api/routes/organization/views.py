

from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import Organization
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
            name = serializer.validated_data.get("name")
            try:
                Organization.objects.get(name=name)
            except ObjectDoesNotExist:
                pass

            organization = Organization(name=name)
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

