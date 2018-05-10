from django.urls import path
from .views import CreateHost, UpdateHost, DeleteHost, generate, UpdateConfig, VariableSet

urlpatterns = [
    path('add/', CreateHost.as_view(), name="create-host"),
    path('update/<int:pk>/', UpdateHost.as_view(), name="update-host"),
    path('delete/<int:pk>/', DeleteHost.as_view(), name="delete-host"),
    path('generate/', generate, name="generate"),
    path('config/edit/<str:slug>/', UpdateConfig.as_view(), name="update-config"),
    path('config/dns-challenge/', VariableSet.as_view(), name="dns-challenge"),
]
