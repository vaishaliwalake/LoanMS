from django.urls import include, path
from rest_framework import routers

from RestWService import views


urlpatterns = [
   # path('Customers',views.CustomersRest,name='Customers'),
  #  path ('CustViewSet', views.CustViewSet, name='CustViewSet'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('chartHome/', views.chartHome, name='chartHome'),
    path('population-chart/', views.population_chart, name='population-chart'),
]



