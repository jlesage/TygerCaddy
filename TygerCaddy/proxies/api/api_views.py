from hosts.caddyfile import caddyfile_build
from proxies.api.serializers import ProxySerializer, HeaderSerializer
from proxies.models import Proxy, Header
from rest_framework import viewsets


class ProxyViewset(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer

    def perform_create(self, serializer):
        serializer.save()
        caddyfile_build()


class HeaderViewset(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer

    def perform_create(self, serializer):
        serializer.save()
        caddyfile_build()
