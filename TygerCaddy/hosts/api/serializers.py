from hosts.models import Host
from proxies.models import Proxy
from rest_framework import serializers


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = ('id','name', 'proxy_from', 'proxy_to', 'load_policy', 'fail_timeout', 'max_fails',
                  'max_conns', 'try_duration', 'try_interval', 'health_check', 'health_check_port',
                  'health_check_interval', 'health_check_timeout', 'keep_alive', 'timeout', 'without',
                  'exceptions', 'insecure_skip_verify', 'websocket', 'transparent', 'host')


class HostSerializer(serializers.ModelSerializer):
    proxy_set = ProxySerializer(many=True, read_only=True)

    class Meta:
        model = Host
        fields = ('id', 'host_name', 'root_path', 'tls', 'staging', 'dns_verification', 'dns_provider',
                  'custom_ssl', 'custom_certs', 'force_redirect_https', 'proxy_set')

