#
# SPDX-License-Identifier: Apache-2.0
#
from api.utils import zipDir
from api.config import CELLO_HOME

from django.core.files.base import File
from rest_framework import viewsets, status
from rest_framework.decorators import action
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
import chardet

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
            node_urls = serializer.validated_data.get("urls")
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
            if node_type == "peer":
                dir_msp = "{}/{}/crypto-config/peerOrganizations/{}/peers/{}/msp"\
                    .format(CELLO_HOME, org_name, org_name, node_name+"."+org_name)
            else:
                dir_msp = "{}/{}/crypto-config/ordererOrganizations/{}/orderers/{}/msp"\
                    .format(CELLO_HOME, org_name, org_name.split(".", 1)[1], node_name+"."+org_name)

            zipDir(dir_msp, "/opt/msp.zip")
            f_msp = open("/opt/msp.zip", "rb")
            print(chardet.detect(f_msp.readline()))

            if node_type == "peer":
                dir_tls = "{}/{}/crypto-config/peerOrganizations/{}/peers/{}/tls" \
                    .format(CELLO_HOME, org_name, org_name, node_name + "." + org_name)
            else:
                dir_tls = "{}/{}/crypto-config/ordererOrganizations/{}/orderers/{}/msp"\
                    .format(CELLO_HOME, org_name, org_name.split(".", 1)[1], node_name+"."+org_name)

            zipDir(dir_tls, "/opt/tls.zip")
            f_tls = open("/opt/tls.zip", "rb")

            node = Node(name=node_name, organization=org, urls=node_urls, type=node_type)
            node.msp.save("msp.zip", File(f_msp))
            node.tls.save("tls.zip", File(f_tls))
            node.save()
            f_msp.close()
            f_tls.close()
            response = NodeIDSerializer(data=node.__dict__)
            if response.is_valid(raise_exception=True):
                return Response(
                    response.validated_data, status=status.HTTP_201_CREATED
                )

    def destroy(self, request, pk=None):
        try:
            node = Node.objects.get(name=pk)
            node.delete()
        except ObjectDoesNotExist:
            raise BaseException

        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        queryset = Node.Objects.all()
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    @action(methods=["post"], detail=True, url_path="operations")
    def operate(self, request, pk=None):
        """
        Operate Node

        Do some operation on node, start/stop/restart
        """
        pass

