from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
    path('angular/', views.AngularView.as_view(), name="angular"),
]