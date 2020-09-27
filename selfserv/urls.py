from django.urls import path
from . import views

urlpatterns = [
    path ('login', views.LoadLoginPage, name='selfserv'),
    path ('validateLogin', views.ValidateLogin, name='selfvalidate'),
    path ('profile', views.profile, name='profile'),
    path ('CustSelfserve', views.CustSelfserve, name='CustSelfserve'),
    path ('CustSaveData', views.CustSaveData, name='CustSaveData'),
    path ('CheckStatus', views.CheckStatus, name='CheckStatus'),
    path('logout', views.logout, name='logout'),
    path ('validatesignUp', views.signupValidate),
    path ('loadsignup', views.loadSignup),

]