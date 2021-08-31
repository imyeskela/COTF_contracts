from main.models import Contract


def get_contracts():
    """Получаем все контракты"""

    return Contract.objects.all()