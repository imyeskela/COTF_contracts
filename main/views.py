from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView

from main.models import Contract
from services.main_logic import get_template_contracts, get_form_contract_template, get_contracts, get_contact
from main.utils import ContractTemplateListAndCreateContractMixin, ContractListMixin, FillingQuestionnaireMixin
from main.forms import ContractTemplateCreateForm, FillingQuestionnaireForm


class ContractTemplateListAndCreateView(ContractTemplateListAndCreateContractMixin, View):
    """Отображение всех контрактов"""

    queryset = get_template_contracts()
    form = get_form_contract_template()
    template_name = 'contract_templates_list.html'


class ContractCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': ContractTemplateCreateForm()}
        return render(request, 'contract_template_creation.html', context)

    def post(self, request, *args, **kwargs):
        form = ContractTemplateCreateForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
        return render(request, 'contract_template_creation.html', {'form': form})


class ContractListView(ContractListMixin, View):
    """Вью для отображения всех Контрактов"""

    queryset = Contract.objects.all()
    template_name = 'contract_list.html'


class FillingQuestionnaireView(FillingQuestionnaireMixin, View):
    """Вью для отображения формы"""
    contract = get_contact
    template_name = 'filling_questionnaire.html'
    form = FillingQuestionnaireForm





