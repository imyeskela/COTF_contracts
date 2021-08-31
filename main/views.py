from django.shortcuts import render
from django.views.generic import View

from services.main_logic import get_contracts
from main.utils import ContractListMixin


class ContractListView(ContractListMixin, View):
    """Отображение всех контрактов"""

    queryset = get_contracts()
    template_name = 'contracts_list.html'