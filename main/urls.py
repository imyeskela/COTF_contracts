from django.urls import path

from main import views

urlpatterns = [
    path('', views.ContractTemplateListAndCreateView.as_view(), name='contract_template_list'),
    path('contracttemplate-creation/', views.ContractCreateView.as_view(), name='tem_form'),
    path('contracts/', views.ContractListView.as_view(), name='contract_list'),
    path('agreement/<contract_number>/', views.FillingQuestionnaireView.as_view(), name='contract_detail')
]