from django.urls import path
from . import views

urlpatterns = [
    path ('UploadCsv', views.UploadCsv, name='upload'),
    path ('uploadPage', views.uploadPage)
]