from django.db import models


class Policies(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

# Create your models here.
class Proxy(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    proxy_from = models.CharField(max_length=255, blank=False, default='/')
    proxy_to = models.CharField(max_length=255, blank=False)
    load_policy = models.ForeignKey(Policies, on_delete=models.CASCADE, blank=True, null=True)
    fail_timeout = models.IntegerField(blank=True, null=True)
    max_fails = models.IntegerField(blank=True, null=True)
    max_conns = models.IntegerField(blank=True, null=True)
    try_duration = models.IntegerField(blank=True, null=True)
    try_interval = models.IntegerField(blank=True, null=True)
    health_check = models.CharField(max_length=255, blank=True, null=True)
    health_check_port = models.CharField(max_length=255, blank=True, null=True)
    health_check_interval = models.CharField(max_length=10, blank=True, null=True)
    health_check_timeout = models.CharField(max_length=10, blank=True, null=True)
    keep_alive = models.IntegerField(blank=True, null=True)
    timeout = models.CharField(max_length=10, blank=True, null=True)
    without = models.CharField(max_length=255, blank=True, null=True)
    exceptions = models.CharField(max_length=255, blank=True, null=True)
    insecure_skip_verify = models.BooleanField(default=False)
    websocket = models.BooleanField(default=False)
    transparent = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Header(models.Model):
    header = models.CharField(max_length=255, blank=False, unique=True)
    upstream = models.BooleanField(default=False)
    downstream = models.BooleanField(default=False)
    value = models.CharField(max_length=255, blank=False)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE)

    def __str__(self):
        return self.header
