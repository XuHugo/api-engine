

from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import Node
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
            name = serializer.validated_data.get("name")
            try:
                Node.objects.get(name=name)
            except ObjectDoesNotExist:
                pass

            node = Node(name=name)
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

