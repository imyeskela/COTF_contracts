import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import CreateView

from cotf_contracts import settings
from main.models import Contract
from services.main_logic import get_template_contracts, get_contracts, get_contract
from main.utils import (
    ContractTemplateListAndCreateContractMixin,
    FillingQuestionnaireMixin,
    AdministrationMixin,
    ContractListMixin,
)
from main.forms import ContractTemplateCreateForm, FillingQuestionnaireForm
from services.getting_form import get_contract_form, get_filling_questionnaire_form, get_contract_template_create_form, \
    get_contract_template_form, get_contract_list_form
from services.ordering import get_ordered_contracts


class ContractTemplateListAndCreateView(ContractTemplateListAndCreateContractMixin, View):
    """Отображение всех контрактов"""

    queryset = get_template_contracts()
    form_contract = get_contract_form()
    form_contract_template = get_contract_template_create_form()
    form_contract_template_change = get_contract_template_form()
    template_name = 'contract_templates_list.html'


class AdministrationView(AdministrationMixin, View):
    template_name = 'administration.html'


# class ContractCreateView(CreateView):
#
#     def get(self, request, *args, **kwargs):
#         context = {'form': ContractTemplateCreateForm()}
#         return render(request, 'contract_templates_list.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = ContractTemplateCreateForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.save()
#             return redirect('contract_template_list')
#         return render(request, 'contract_templates_list.html', {'create_template': form})


class ContractListView(ContractListMixin, View):
    """Вью для отображения всех Контрактов"""

    queryset = get_ordered_contracts
    template_name = 'contract_list.html'
    form_contract_template = get_contract_template_create_form()
    form_contract = get_contract_list_form()


class FillingQuestionnaireView(FillingQuestionnaireMixin, View):
    """Вью для отображения формы"""
    contract = get_contract
    template_name = 'filling_questionnaire.html'
    form = FillingQuestionnaireForm


# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#
#             response = HttpResponse(fh.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
#             return response


