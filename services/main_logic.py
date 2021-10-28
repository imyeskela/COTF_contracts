from django.shortcuts import get_object_or_404

from main.models import ContractTemplate, Contract, AuthenticationCode


def get_template_contracts():
    """Получаем все Шаблоны Контракты"""

    return ContractTemplate.objects.all()


def get_contracts():
    """Получаем все Контракты"""

    return Contract.objects.all()


def get_contract(self):
    return get_object_or_404(Contract.objects.all(), number=self.kwargs['contract_number'])


def generator_num_contract():
    """Генератор номера договора"""

    try:
        contract = Contract.objects.last()
        contract_num = getattr(contract, 'number')
        return contract_num + 1
    except AttributeError:
        return 24546799


def get_code_obj(self):
    return AuthenticationCode.objects.filter(contract=get_contract(self))


def get_codes_of_obj():
    codes = AuthenticationCode.objects.values_list('code', flat=True)
    return codes


def get_num_attempts(self):
    number_of_attempts = get_code_obj(self)
    return number_of_attempts



