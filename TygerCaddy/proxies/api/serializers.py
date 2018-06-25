from proxies.models import Proxy, Header
from rest_framework import serializers


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = ('name', 'proxy_from', 'proxy_to', 'load_policy', 'fail_timeout', 'max_fails',
                  'max_conns', 'try_duration', 'try_interval', 'health_check', 'health_check_port',
                  'health_check_interval', 'health_check_timeout', 'keep_alive', 'timeout', 'without',
                  'exceptions', 'insecure_skip_verify', 'websocket', 'transparent', 'host')


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ('header', 'upstream', 'downstream', 'value', 'proxy')