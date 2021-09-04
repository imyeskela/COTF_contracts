from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


class ContractListMixin:
    """Миксин для отображения всех контрактов"""

    queryset = None
    template_name = None
    form = None

    def get(self, request):
        return render(request, self.template_name, {'contract_list': self.queryset, 'form': self.form, })

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            contact_template_id = int(request.POST.get('contract_template'))
            contract_template = self.queryset.get(id=contact_template_id)
            print(contract_template)
            form = form.save(commit=False)
            form.amount = int(request.POST.get('amount_bitch'))
            form.contract_template = contract_template
            form.save()

        return render(request, 'contracts_list.html', {'form': form})
