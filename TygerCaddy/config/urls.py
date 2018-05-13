from django.urls import path
from .views import UpdateConfig, VariableSet

urlpatterns = [
    path('edit/<str:slug>/', UpdateConfig.as_view(), name="update-config"),
    path('dns-challenge/', VariableSet.as_view(), name="dns-challenge"),
]
