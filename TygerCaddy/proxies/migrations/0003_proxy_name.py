# Generated by Django 2.0.3 on 2018-05-13 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0002_remove_proxy_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='name',
            field=models.CharField(default='name', max_length=255),
            preserve_default=False,
        ),
    ]
