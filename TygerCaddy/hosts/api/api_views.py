from hosts.api.serializers import HostSerializer
from hosts.caddyfile import caddyfile_build
from hosts.models import Host
from rest_framework import viewsets


class HostViewset(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    def perform_create(self, serializer):
        serializer.save()
        caddyfile_build()
