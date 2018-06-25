from config.models import Config
from rest_framework import serializers


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('name', 'interface', 'port', 'proxy_host', 'proxy_exception', 'root_dir',
                  'dns_challenge', 'dns_provider', 'ssl_staging')
