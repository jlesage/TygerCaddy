from django.contrib import admin

from .models import Proxy, Header, Policies

# Register your models here.

admin.site.register(Proxy)
admin.site.register(Header)
admin.site.register(Policies)
