from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from services.main_logic import generator_num_contract
from services.questionnaire import form_questionnaire, finally_rich, get_sign_img, create_new_code_obj


class ContractTemplateListAndCreateContractMixin:
    """Миксин для отображения всех шаблонов контрактов"""

    queryset = None
    template_name = None
    form_contract = None
    form_contract_template = None

    def get(self, request):
        paginator = Paginator(self.queryset, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'contract_template_list': page_obj,
                                                    'form_contract': self.form_contract,
                                                    'form_contract_template': self.form_contract_template
                                                    })

    def post(self, request):
        form_contract = self.form_contract(request.POST)
        form_contract_template = self.form_contract_template(request.POST, request.FILES)
        if 'form_contract' in request.POST:
            if form_contract.is_valid():
                contact_template_id = int(request.POST.get('contract_template'))
                contract_template = self.queryset.get(id=contact_template_id)
                form_contract = form_contract.save(commit=False)
                form_contract.amount = int(request.POST.get('amount_bitch'))
                form_contract.contract_template = contract_template
                form_contract.number = generator_num_contract()
                print('fc')
                form_contract.save()
                return redirect('contract_list')
            else:
                return render(request, self.template_name, {'form_contract': form_contract, 'form_contract_template': form_contract_template})
        if 'form_contract_template' in request.POST:
            if form_contract_template.is_valid():
                form_contract_template = form_contract_template.save(commit=False)
                form_contract_template.save()
                return redirect('contract_template_list')
            else:
                return render(request, self.template_name,
                              {'form_contract_template': form_contract_template})

        return render(request, self.template_name, {'form_contract': form_contract, 'form_contract_template': form_contract_template})


class ContractListMixin:
    """Миксин для отображения всех контрактов"""

    queryset = None
    template_name = None
    form_contract_template = None

    def get(self, request):
        paginator = Paginator(self.queryset, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        template_name = self.template_name
        return render(request, template_name, {'contract_list': page_obj, 'form_contract_template': self.form_contract_template})

    def post(self, request):
        form_contract_template = self.form_contract_template(request.POST, request.FILES)
        if form_contract_template.is_valid():
            form_contract_template = form_contract_template.save(commit=False)
            form_contract_template.save()
            return redirect('contract_template_list')
        else:
            return render(request, self.template_name,
                          {'form_contract_template': form_contract_template})


class FillingQuestionnaireMixin:
    """Миксин для формы анкета"""

    form = None
    contract = None
    template_name = None

    def get(self, request, contract_number):
        return render(request, self.template_name, {'form': self.form, 'contract': self.contract})

    def post(self, request, contract_number):
        form = self.form(request.POST)
        if 'code' in request.POST:
            create_new_code_obj(self, request, contract_number)
            return render(request, 'filling_questionnaire.html', {'form': form})

        elif 'docx' in request.POST:
            docx_base = form_questionnaire(self, request, contract_number)
            return render(request, 'filling_questionnaire.html', {'docx_base': docx_base, 'form': form})

        elif 'qr_code' in request.POST:
            img_base = finally_rich(self, request, contract_number)
            get_sign_img(self, request, contract_number)
            return render(request, 'filling_questionnaire.html', {'img_base': img_base})

        return render(request, 'filling_questionnaire.html', {'form': form})



