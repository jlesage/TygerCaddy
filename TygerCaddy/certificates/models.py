import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse


def get_cert_path(instance, filename):
    return os.path.join('sites', filename)


class Bundle(models.Model):
    bundle_file = models.FileField(upload_to=get_cert_path, blank=False, null=False)


class Key(models.Model):
    key_file = models.FileField(upload_to=get_cert_path, blank=False, null=False)


class Certificate(models.Model):
    cert_name = models.CharField(max_length=200, blank=False, unique=True)
    bundle_upload = models.ForeignKey(Bundle, on_delete=models.CASCADE, blank=True, null=True)
    key_upload = models.ForeignKey(Key, on_delete=models.CASCADE, blank=True, null=True)
    bundle_text = models.TextField(max_length=500, blank=True, null=True)
    key_text = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.cert_name

    def get_absolute_url(self):
        return reverse('cert-detail', kwargs={'cert': self.cert_name})


@receiver(models.signals.post_delete, sender=Bundle)
def auto_delete_bundle_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Bundle` object is deleted.
    """
    if instance.bundle_file:
        if os.path.isfile(instance.bundle_file.path):
            os.remove(instance.bundle_file.path)


@receiver(models.signals.pre_save, sender=Bundle)
def auto_delete_bundle_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Bundle` object is updated
    with new file.
    """
    if not instance.pk:
        return False


@receiver(models.signals.post_delete, sender=Key)
def auto_delete_key_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Bundle` object is deleted.
    """
    if instance.key_file:
        if os.path.isfile(instance.key_file.path):
            os.remove(instance.key_file.path)


@receiver(models.signals.pre_save, sender=Key)
def auto_delete_key_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Bundle` object is updated
    with new file.
    """
    if not instance.pk:
        return False
