from django.core.exceptions import ValidationError

from main.models import ContractTemplate


def get_contracts():
    """Получаем все контракты"""

    return ContractTemplate.objects.all()


def _is_valid(value):
    """Проверка на пустое поле"""

    return value != '' and value is not None


def check_file_for_vars(self):
    update = self.request.GET.get('update')

    if _is_valid(update):
        pass

