from django.contrib import admin
from .models import Proxy, Header, Policies
# Register your models here.

admin.register(Proxy)
admin.register(Header)
admin.register(Policies)