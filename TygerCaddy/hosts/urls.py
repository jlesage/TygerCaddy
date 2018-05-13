from django.urls import path
from .views import CreateHost, UpdateHost, DeleteHost, generate, AllHosts

urlpatterns = [
    path('list/', AllHosts.as_view(), name="all-hosts"),
    path('add/', CreateHost.as_view(), name="create-host"),
    path('update/<int:pk>/', UpdateHost.as_view(), name="update-host"),
    path('delete/<int:pk>/', DeleteHost.as_view(), name="delete-host"),
    path('generate/', generate, name="generate"),
]
