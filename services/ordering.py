from django.db.models import Q

from main.models import Contract
from services.main_logic import get_contracts


def _is_valid(value):
    """Проверка на пустое поле"""

    return value != '' and value is not None


def get_ordered_contracts(self):
    qs_contracts = get_contracts()

    all_contracts = self.request.GET.get('all_contracts')
    contract_number_min = self.request.GET.get('contract_number_min')
    contract_number_max = self.request.GET.get('contract_number_max')

    date_created_min = self.request.GET.get('date_created_min')
    date_created_max = self.request.GET.get('date_created_max')

    date_signed_min = self.request.GET.get('date_signed_min')
    date_signed_max = self.request.GET.get('date_signed_max')

    status_min = self.request.GET.get('status_min')
    status_max = self.request.GET.get('status_max')

    search_objs = self.request.GET.get('search')

    if _is_valid(all_contracts):
        qs_contracts = qs_contracts

    if _is_valid(contract_number_min):
        qs_contracts = qs_contracts.order_by('number')
    if _is_valid(contract_number_max):
        qs_contracts = qs_contracts.order_by('-number')

    if _is_valid(date_created_min):
        qs_contracts = qs_contracts.order_by('date_created')
    if _is_valid(date_created_max):
        qs_contracts = qs_contracts.order_by('-date_created')

    if _is_valid(date_signed_min):
        qs_contracts = qs_contracts.order_by('date_signed')
    if _is_valid(date_signed_max):
        qs_contracts = qs_contracts.order_by('-date_signed')

    if _is_valid(status_min):
        qs_contracts = qs_contracts.order_by('status')
    if _is_valid(status_max):
        qs_contracts = qs_contracts.order_by('-status')

    if _is_valid(search_objs):
        qs_contracts = qs_contracts.filter(
            Q(full_name__icontains=search_objs) | Q(identifier__icontains=search_objs)
        )
        # qs_contracts = qs_contracts.annotate(search=SearchVector(
        #     'full_name',
        #     'name',
        #     'identifier'
        # )).filter(search=search_objs)

    return qs_contracts
