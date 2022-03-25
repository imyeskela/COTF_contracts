from django.urls import path
from django.conf.urls.static import static
from django.views.static import serve

from cotf_contracts import settings
from main import views
from services.download import download
urlpatterns = [
    path('', views.ContractTemplateListAndCreateView.as_view(), name='contract_template_list'),
    path('contracts/', views.ContractListView.as_view(), name='contract_list'),
    path('agreement/<contract_number>/', views.FillingQuestionnaireView.as_view(), name='contract_detail'),
    path('administration/', views.AdministrationView.as_view(), name='administration')
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
