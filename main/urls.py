from django.urls import path

from main import views

urlpatterns = [
    path('', views.doc_test, name='contract_list'),
    path('contract-creation/', views.ContractCreateView.as_view(), name='tem_form')
]