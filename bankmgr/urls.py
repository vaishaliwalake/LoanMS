from django.urls import path
from . import views


urlpatterns = [

    path('loanApprovals', views.BankMngr),
    path ('validate', views.LoanValidation, name='validate'),
    path('ApproveLoanRequest',views.ApproveLoanRequest),
    path('charts',views.loanMDMChartView)


]