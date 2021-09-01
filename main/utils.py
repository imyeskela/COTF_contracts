from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


class ContractListMixin:
    """Миксин для отображения всех контрактов"""

    queryset = None
    template_name = None

    def get(self, request):

        return render(request, self.template_name, {'contract_list': self.queryset})
