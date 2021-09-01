from django.urls import path

from main import views

urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract_list'),
    path('contract-creation/', views.ContractCreateView.as_view(), name='tem_form')
]