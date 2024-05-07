from django.urls import path, include
from procData import views

urlpatterns = [
    path('', views.breachStructure_list, name="breachStructure_list"),
    path('<str:email>', views.breachStructure_detail, name="breachStructure_detail"),
    path('uploadCSV/', views.upload_csv, name='upload_csv'),
    path('success_url/', views.success_url, name='success_url'),
    path('list_users/', views.show_allusers, name="show_allusers"),
]