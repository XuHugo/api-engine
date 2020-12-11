

from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import NetWork, Node, Organization
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
            organizations = serializer.validated_data.get("organizations")
            try:
                NetWork.objects.get(name=network_name)
            except ObjectDoesNotExist:
                pass
            orderers = []
            peers = []
            i = 0
            for organization in organizations:
                org = Organization.objects.get(name=organization)
                orderers.append({"name":organization, "hosts":[]})
                peers.append({"name":organization, "hosts":[]})
                nodes = Node.objects.filter(organization=org)
                for node in nodes:
                    if node.type == "peer":
                        peers[i]["hosts"].append({"name": node.name, "port": node.urls.split(":")[2]})
                    elif node.type == "orderer":
                        orderers[i]["hosts"].append({"name": node.name, "port": node.urls.split(":")[2]})
                i = i+1

            ConfigTX(network_name).create(consensus=consensus, orderers=orderers, peers=peers)
            ConfigTxGen(network_name).genesis()

            network = NetWork(name=network_name)
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

