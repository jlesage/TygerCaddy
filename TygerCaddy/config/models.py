from django.db import models
from dns.models import DNS


# Create your models here.
class Config(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    interface = models.CharField(max_length=200, blank=False, unique=True)
    port = models.IntegerField(blank=False, unique=True)
    proxy_host = models.CharField(max_length=200, blank=False)
    proxy_exception = models.CharField(max_length=200, blank=False)
    root_dir = models.CharField(max_length=200, blank=False)
    dns_challenge = models.BooleanField(default=False)
    dns_provider = models.ForeignKey(DNS, on_delete=models.CASCADE, related_name='dns_name', blank=True, null=True)
    ssl_staging = models.BooleanField(default=False)