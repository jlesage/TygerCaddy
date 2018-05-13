from django.db import models
from django.urls import reverse
from dns.models import DNS
from proxies.models import Proxy
# Create your models here.


class Host(models.Model):
    host_name = models.CharField(max_length=200, blank=False, unique=True)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, blank=True, null=True)
    root_path = models.CharField(max_length=200, blank=True)
    tls = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('host-detail', kwargs={'host': self.host_name})