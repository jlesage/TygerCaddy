from hosts.models import Host
from rest_framework import serializers


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('host_name', 'root_path', 'tls', 'staging', 'dns_verification', 'dns_provider',
                  'custom_ssl', 'custom_certs', 'force_redirect_https')
