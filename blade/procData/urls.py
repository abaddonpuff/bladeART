from django.urls import path, include
from procData import views

urlpatterns = [
    path('', views.breachStructure_list, name="breachStructure_list"),
    path('<str:email>', views.breachStructure_detail, name="breachStructure_detail"),
]