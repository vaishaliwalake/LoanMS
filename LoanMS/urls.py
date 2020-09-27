"""LoanMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path
from rest_framework import routers
from RestWService import views
router = routers.DefaultRouter()
#router.register(r'cust', views.CustomersRest, 'customer')


urlpatterns = [

    path ('', include ("home.urls")),
    path ('selfserv/', include ("selfserv.urls")),
    path ('bankmgr/', include ("bankmgr.urls")),
    #path('',include('home.urls')),
    # path('bankmgr/',include('bankmgr.urls')),
    # path('bulkops/',include('bulkops.urls')),
    path('mdmteam/',include('mdmteam.urls')),
   #path('users/', include('users.urls')), # new
    path('users/', include('django.contrib.auth.urls')), # new
    path('admin/', admin.site.urls),
    path('UploadCSV/', include('UploadCSV.urls')),
    path ('RestWService/', include ('RestWService.urls')),


                  # path('selfserv/',include('selfserv.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
