from django.contrib import admin
from .models import Proxy, Headers, Policies
# Register your models here.

admin.register(Proxy)
admin.register(Headers)
admin.register(Policies)