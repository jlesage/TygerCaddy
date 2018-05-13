from django.db import models

class Policies(models.Model):
    name = models.CharField(max_length=255, blank=False)


# Create your models here.
class Proxy(models.Model):
    proxy_from = models.CharField(max_length=255, blank=False, default='/')
    proxy_to = models.CharField(max_length=255, blank=False)
    load_policy = models.ForeignKey(Policies, on_delete=models.CASCADE, blank=True)
    fail_timeout = models.IntegerField(blank=True)
    max_fails = models.IntegerField(blank=True)
    max_conns = models.IntegerField(blank=True)
    try_duration = models.IntegerField(blank=True)
    try_interval = models.IntegerField(blank=True)
    health_check = models.CharField(max_length=255, blank=True)
    health_check_port = models.CharField(max_length=255, blank=True)
    health_check_interval = models.IntegerField(blank=True)
    health_check_timeout = models.IntegerField(blank=True)
    keep_alive = models.IntegerField(blank=True)
    timeout = models.IntegerField(blank=True)
    without = models.CharField(max_length=255, blank=True)
    exceptions = models.CharField(max_length=255, blank=True)
    insecure_skip_verify = models.BooleanField(default=False)
    websocket = models.BooleanField(default=False)
    transparent = models.BooleanField(default=False)


class Headers(models.Model):
    header = models.CharField(max_length=255, blank=False)
    upstream = models.BooleanField(default=False)
    downstream = models.BooleanField(default=False)
    value = models.CharField(max_length=255, blank=False)
    proxy = models.ManyToManyField(Proxy)

