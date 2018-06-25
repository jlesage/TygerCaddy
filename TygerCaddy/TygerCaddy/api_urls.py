from django.conf.urls import url, include
from rest_framework import routers
from hosts.api.api_views import HostViewset
from proxies.api.api_views import ProxyViewset, HeaderViewset
from config.api.api_views import ConfigViewset

router = routers.DefaultRouter()
router.register(r'hosts', HostViewset)
router.register(r'proxies', ProxyViewset)
router.register(r'headers', HeaderViewset)
router.register(r'config', ConfigViewset)
