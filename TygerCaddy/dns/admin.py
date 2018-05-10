from django.contrib import admin

# Register your models here.
from .models import DNS, EVariables

admin.site.register(DNS)
admin.site.register(EVariables)
