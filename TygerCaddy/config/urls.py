from django.urls import path

from .views import UpdateConfig

urlpatterns = [
    path('edit/<str:slug>/', UpdateConfig.as_view(), name="update-config"),

]
