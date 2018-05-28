# Generated by Django 2.0.3 on 2018-05-20 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dns', '0004_auto_20180510_1648'),
        ('hosts', '0010_host_staging'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='dns_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dns.DNS'),
        ),
        migrations.AddField(
            model_name='host',
            name='dns_verification',
            field=models.BooleanField(default=False),
        ),
    ]