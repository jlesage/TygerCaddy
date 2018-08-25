
from certificates.models import Certificate
from django.db import models
from django.urls import reverse
from dns.models import DNS


# Create your models here.


class Host(models.Model):
    host_name = models.CharField(max_length=200, blank=False, unique=True)
    root_path = models.CharField(max_length=200, blank=True)
    tls = models.BooleanField(default=True)
    staging = models.BooleanField(default=False)
    dns_verification = models.BooleanField(default=False)
    dns_provider = models.ForeignKey(DNS, on_delete=models.CASCADE, blank=True, null=True)
    custom_ssl = models.BooleanField(default=False)
    custom_certs = models.ManyToManyField(Certificate, blank=True)
    force_redirect_https = models.BooleanField(default=True)
    basic_auth = models.BooleanField(default=False)
    basic_username = models.CharField(max_length=200, blank=True, null=True)
    basic_password = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.host_name

    def get_absolute_url(self):
        return reverse('host-detail', kwargs={'host': self.host_name})