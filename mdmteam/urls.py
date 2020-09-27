from django.urls import path, include


from . import views

urlpatterns = [
    path('mdm/', views.mdm),
    path('reports', views.reports,name='create'),
    path('mdmform_view',views.loanManager),
    path('deletereport', views.deletereport,name='deletereport'),
    path('report_update',views.report_update,name='edit'),
    path ('UploadCsv', views.UploadCsv, name='upload'),
    path ('uploadPage', views.uploadPage),
    path ('loadEditreportById', views.loadEditreportById, name='loadEditreportById'),
    path('RestView',views.RestView.as_view(),name='RestView')

]