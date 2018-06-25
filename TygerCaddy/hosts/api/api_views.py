from hosts.models import Host
from rest_framework import viewsets
from hosts.api.serializers import HostSerializer


class HostViewset(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
