from proxies.models import Proxy, Header
from rest_framework import viewsets
from proxies.api.serializers import ProxySerializer, HeaderSerializer


class ProxyViewset(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer


class HeaderViewset(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer
