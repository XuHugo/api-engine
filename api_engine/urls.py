"""api_engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.routes.organization.views import OrganizationViewSet
from api.routes.agent.views import AgentViewSet
from api.routes.network.views import NetWorkViewSet
from api.routes.node.views import NodeViewSet



# define and register routers of api
router = DefaultRouter(trailing_slash=False)
router.register("organizations", OrganizationViewSet, basename="organization")
router.register("agents", AgentViewSet, basename="agent")
router.register("networks", NetWorkViewSet, basename="network")
router.register("nodes", NodeViewSet, basename="node")


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
