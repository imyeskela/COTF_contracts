from django.shortcuts import get_object_or_404


from main.models import ContractTemplate, Contract
from main.forms import ContractTemplateCreateForm, ContractCreateForm, FillingQuestionnaireForm


def get_template_contracts():
    """Получаем все Шаблоны Контракты"""

    return ContractTemplate.objects.all()


def get_form_contract_template():
    """Получаем форму для создания Контракта"""

    return ContractCreateForm


def get_contracts():
    """Получаем все Контракты"""

    return Contract.objects.all()


def get_filling_questionnaire_form():
    """Получаем форму для заполнение анкеты"""

    return FillingQuestionnaireForm


def get_contact(self):
    return get_object_or_404(Contract.objects.all(), number=self.kwargs['contract_number'])


def generator_num_contract():
    """Генератор номера договора"""

    try:
        contract = Contract.objects.last()
        contract_num = getattr(contract, 'number')
        return contract_num + 1
    except AttributeError:
        return 24546799


