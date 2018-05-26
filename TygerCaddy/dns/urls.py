from django.urls import path

from .views import Providers, SetVariables

urlpatterns = [
    path('set_variables/<slug:dns>/', SetVariables.as_view(), name="set-vars"),
    path('all', Providers.as_view(), name="dns-providers"),
]
