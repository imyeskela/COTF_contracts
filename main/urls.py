from django.urls import path

from main import views

urlpatterns = [
    path('', views.ContractListView.as_view(), name='contracts')
]