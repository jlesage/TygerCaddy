from django.urls import path
from .views import CreateProxy, ListProxies, UpdateProxy, DeleteProxy, DetailProxy, CreateHeader, ListHeaders, UpdateHeader, DeleteHeader, DetailHeader

urlpatterns = [
    path('add/', CreateProxy.as_view(), name="create-proxy"),
    path('list/', ListProxies.as_view(), name="all-proxies"),
    path('detail/<int:pk>/', DetailProxy.as_view(), name="proxy-detail"),
    path('update/<int:pk>/', UpdateProxy.as_view(), name="update-proxy"),
    path('delete/<int:pk>/', DeleteProxy.as_view(), name="delete-proxy"),
    path('headers/add/', CreateHeader.as_view(), name="create-header"),
    path('headers/list/', ListHeaders.as_view(), name="all-headers"),
    path('headers/detail/<int:pk>/', DetailHeader.as_view(), name="header-detail"),
    path('headers/update/<int:pk>/', UpdateHeader.as_view(), name="update-header"),
    path('headers/delete/<int:pk>/', DeleteHeader.as_view(), name="delete-header"),
]
