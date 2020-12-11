

from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import Node, Organization
from api.lib.pki import CryptoGen, CryptoConfig
from django.core.exceptions import ObjectDoesNotExist
from api.routes.node.serializers import (
    NodeSerializer,
    NodeCreateBody,
    NodeIDSerializer,
    NodeQuery,
)


class NodeViewSet(viewsets.ViewSet):

    def list(self, request):

        queryset = Node.objects.all()
        serializer = NodeSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        serializer = NodeCreateBody(data=request.data)

        if serializer.is_valid(raise_exception=True):
            node_name = serializer.validated_data.get("name")
            node_type = serializer.validated_data.get("type")
            organization = serializer.validated_data.get("organization")
            org_name = organization["name"]
            try:
                Node.objects.get(name=node_name)
            except ObjectDoesNotExist:
                pass

            org = Organization.objects.get(name=org_name)

            nodes = {
                "type": node_type,
                "Specs": [node_name]
            }
            CryptoConfig(org_name).update(nodes)
            CryptoGen(org_name).extend()

            node = Node(name=node_name, organization=org)
            node.save()

            response = NodeIDSerializer(data=node.__dict__)
            if response.is_valid(raise_exception=True):
                return Response(
                    response.validated_data, status=status.HTTP_201_CREATED
                )

    def destroy(self, request, pk=None):
        pass

    def retrieve(self, request, pk=None):
        queryset = Node.Objects.all()
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass
