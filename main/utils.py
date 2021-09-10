from django.shortcuts import render
import os
from docxtpl import DocxTemplate
from babel.dates import format_date

import base64

from cotf_contracts.settings import BASE_DIR
from services.main_logic import generator_num_contract


class ContractTemplateListAndCreateContractMixin:
    """Миксин для отображения всех шаблонов контрактов"""

    queryset = None
    template_name = None
    form = None

    def get(self, request):
        return render(request, self.template_name, {'contract_template_list': self.queryset, 'form': self.form, })

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            contact_template_id = int(request.POST.get('contract_template'))
            contract_template = self.queryset.get(id=contact_template_id)
            form = form.save(commit=False)
            form.amount = int(request.POST.get('amount_bitch'))
            form.contract_template = contract_template
            form.number = generator_num_contract()
            form.save()

        return render(request, self.template_name, {'form': form})


class ContractListMixin:
    """Миксин для отображения всех контрактов"""

    queryset = None
    template_name = None

    def get(self, request):
        queryset = self.queryset
        template_name = self.template_name
        return render(request, template_name, {'contract_list': queryset})


class FillingQuestionnaireMixin:
    """Миксин для формы анкета"""

    form = None
    contract = None
    template_name = None

    def get(self, request, contract_number):
        return render(request, self.template_name, {'form': self.form, 'contract': self.contract})

    def post(self, request, contract_number):
        form = self.form(request.POST)
        contract = self.contract()
        if form.is_valid:
            docx = DocxTemplate(os.path.join(BASE_DIR, contract.contract_template.template_of_contract.path))
            # basic_vars = ['email', 'passport', 'signature', 'full_name',
            #               'id', 'generated_date', 'short_name', 'phone']
            #
            # renewal_vars = ['sum', 'email', 'passport', 'signature', 'text_sum',
            #                 'full_name', 'id', 'generated_date', 'short_name', 'phone']
            last_name = request.POST['last_name']
            name = request.POST['name']
            sur_name = request.POST['sur_name']
            full_name = last_name.title() + ' ' + name.title() + ' ' + sur_name.title()
            generated_date = format_date(contract.date_created, 'd MMMM yyyy', locale='ru')
            phone = str(request.POST['phone'])
            passport = request.POST['passport']
            email = request.POST['email']

            if sur_name:
                short_name = last_name + ' ' + name[0] + '.' + sur_name[0] + '.'
            else:
                short_name = last_name + ' ' + name[0] + '.'

            id_contract = str(contract.number)
            path_docx = os.path.join(BASE_DIR, 'upload\\tmp\\' + id_contract + '.docx')

            if str(contract.contract_template.type) == 'Основной':
                basic_vars = {'email': email,
                              'full_name': full_name,
                              'id': id_contract,
                              'short_name': short_name,
                              'generated_date': generated_date,
                              'phone': phone,
                              'passport': passport}
                docx.render(basic_vars)

                docx.save(path_docx)
            else:
                pass

            docx_open = open(path_docx, 'rb')
            docx_read = docx_open.read()
            docx_base = base64.b64encode(docx_read)
            docx_open.close()
            os.remove(path_docx)
            return render(request, self.template_name, {'form': form, 'base64': docx_base})
        else:
            form = self.form()

