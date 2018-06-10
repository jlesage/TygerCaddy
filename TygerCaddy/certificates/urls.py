from django.urls import path

from .views import CreateCertificate, UpdateCertificate, DeleteCertificate, AllCertificate, UploadCertificate

urlpatterns = [
    path('list/', AllCertificate.as_view(), name="all-certificates"),
    path('create/', CreateCertificate.as_view(), name="create-certificate"),
    path('upload/', UploadCertificate.as_view(), name="upload-certificate"),
    path('update/<int:pk>/', UpdateCertificate.as_view(), name="update-certificate"),
    path('delete/<int:pk>/', DeleteCertificate.as_view(), name="delete-certificate"),
]
