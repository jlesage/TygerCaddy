from django.contrib import admin

# Register your models here.
from .models import Host, Config

admin.site.register(Host)
admin.site.register(Config)
