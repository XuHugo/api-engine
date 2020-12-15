
from rest_framework import viewsets, status
from api.models import Agent, Organization
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from api.routes.agent.serializers import (
    AgentSerializer,
    AgentCreateBody,
    AgentIDSerializer,
    AgentQuery,
)


class AgentViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Agent.objects.all()
        serializer = AgentSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        serializer = AgentCreateBody(data=request.data)
        if serializer.is_valid(raise_exception=True):
            agent_name = serializer.validated_data.get("name")
            agent_type = serializer.validated_data.get("type")
            agent_urls = serializer.validated_data.get("urls")
            agent_org = serializer.validated_data.get("organization")
            org_name = agent_org["name"]
            try:
                Agent.objects.get(name=agent_name)
            except ObjectDoesNotExist:
                pass
            org = Organization.objects.get(name=org_name)

            agent = Agent(name=agent_name, type=agent_type, urls=agent_urls, organization=org)
            agent.save()

            response = AgentIDSerializer(data=agent.__dict__)
            if response.is_valid(raise_exception=True):
                return Response(
                    response.validated_data, status=status.HTTP_201_CREATED
                )

    def destroy(self, request, pk=None):
        try:
            agent = Agent.objects.get(name=pk)
            if agent.organization:
                raise BaseException
            agent.delete()
        except ObjectDoesNotExist:
            raise BaseException

        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        queryset = Agent.Objects.all()
        serializer = AgentSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass