from django.urls import path
from .views import LogsIndex

urlpatterns = [
    path('', LogsIndex.as_view(), name="all-logs"),
]
