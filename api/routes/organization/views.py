

from rest_framework import viewsets, status
from api.models import Organization

class OrganizationViewSet(viewsets.ViewSet):

    def create(self, request):
        pass

    def get(self, request):

        data = Organization.Objects.all()
        pass

