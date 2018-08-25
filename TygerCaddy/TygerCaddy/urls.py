"""TygerCaddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from hosts.views import generate, reload

from .api_urls import router

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/')),
    path('install/', include('install.urls')),
    path('dns/', include('dns.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('hosts/', include('hosts.urls')),
    path('proxies/', include('proxies.urls')),
    path('certificates/', include('certificates.urls')),
    path('logs/', include('logs.urls')),
    path('config/', include('config.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.login, {'template_name': 'dashboard/login.html'}, name='login'),
    path('accounts/logout/', auth_views.logout, {'next_page': '/accounts/login'}, name='logout'),
    path('accounts/password/change/', auth_views.password_change, {'template_name': 'dashboard/pass-change.html'},  name='update-password'),
    path('accounts/password/change/done/', auth_views.password_change_done, {'template_name': 'dashboard/pass-change-done.html'}, name='password_change_done'),
    path('v2/', TemplateView.as_view(template_name='angular/index.html'), name='angular_v2'),
]

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/generate/', generate, name="generate"),
    path('api/reload/', reload, name="generate"),
    path('api-auth/', include('rest_auth.urls'))
]
