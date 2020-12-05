

from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import NetWork
from api.lib.configtxgen import ConfigTX, ConfigTxGen
from django.core.exceptions import ObjectDoesNotExist
from api.routes.network.serializers import (
    NetWorkSerializer,
    NetWorkCreateBody,
    NetWorkIDSerializer,
    NetWorkQuery,
)


class NetWorkViewSet(viewsets.ViewSet):

    def list(self, request):

        queryset = NetWork.objects.all()
        serializer = NetWorkSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = NetWorkCreateBody(data=request.data)
        if serializer.is_valid(raise_exception=True):
            network_name = serializer.validated_data.get("name")
            consensus = serializer.validated_data.get("consensus")
            peers = serializer.validated_data.get("peers")
            orderers = serializer.validated_data.get("orderers")
            try:
                NetWork.objects.get(name=network_name)
            except ObjectDoesNotExist:
                pass

            ConfigTX(network_name).create(consensus=consensus, orderers=orderers, peers=peers)

            ConfigTxGen(network_name).genesis()

            network = NetWork(network_name)
            network.save()

            response = NetWorkIDSerializer(data=network.__dict__)
            if response.is_valid(raise_exception=True):
                return Response(
                    response.validated_data, status=status.HTTP_201_CREATED
                )

    def destroy(self, request, pk=None):
        pass

    def retrieve(self, request, pk=None):
        queryset = NetWork.Objects.all()
        serializer = NetWorkSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

