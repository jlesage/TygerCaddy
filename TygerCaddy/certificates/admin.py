from django.contrib import admin

# Register your models here.
from .models import Certificate, Bundle, Key

admin.site.register(Certificate)
admin.site.register(Bundle)
admin.site.register(Key)
