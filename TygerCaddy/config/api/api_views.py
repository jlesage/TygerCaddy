from config.models import Config
from rest_framework import viewsets
from config.api.serializers import ConfigSerializer


class ConfigViewset(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
