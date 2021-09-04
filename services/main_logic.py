from django.core.exceptions import ValidationError

from main.models import ContractTemplate
from main.forms import ContractTemplateCreateForm, ContractCreateForm


def get_contracts():
    """Получаем все контракты"""

    return ContractTemplate.objects.all()


def get_form_contract_template():
    return ContractCreateForm



