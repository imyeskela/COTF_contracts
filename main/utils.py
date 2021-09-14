from io import BytesIO

from django.http import JsonResponse
from django.shortcuts import render, redirect
import os
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from babel.dates import format_date
from PIL import Image
from docx import Document
from docx.shared import Mm, Inches, Pt
import qrcode


import base64

from cotf_contracts.settings import BASE_DIR
from services.main_logic import generator_num_contract
from services.num_to_text import num2text


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
            return redirect('contract_list')
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
        if request.GET.get('ready') == 'ready':
            print('user clicked summary')
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
            phone = request.POST['phone']
            passport = request.POST['passport']
            email = request.POST['email']
            if sur_name:
                short_name = last_name + ' ' + name[0] + '.' + sur_name[0] + '.'
            else:
                short_name = last_name + ' ' + name[0] + '.'

            id_contract = str(contract.number)
            path_docx = os.path.join(BASE_DIR, 'upload\\tmp\\' + id_contract + '.docx')
            type = str(contract.contract_template.type)
            if type == 'Основной':
                basic_vars = {'email': email,
                              'full_name': full_name,
                              'id': id_contract,
                              'short_name': short_name,
                              'generated_date': generated_date,
                              'phone': phone,
                              'passport': passport,

                              }
                docx.render(basic_vars)

                docx.save(path_docx)
            else:
                sum = contract.amount
                text_sum = num2text(sum) + ' рублей'
                renewal_vars = {'email': email,
                                'full_name': full_name,
                                'id': id_contract,
                                'short_name': short_name,
                                'generated_date': generated_date,
                                'phone': phone,
                                'passport': passport,
                                'sum': str(sum),
                                'text_sum': text_sum
                                }
                docx.render(renewal_vars)

                docx.save(path_docx)

            docx_open = open(path_docx, 'rb')
            docx_read = docx_open.read()
            docx_base = base64.b64encode(docx_read)
            docx_open.close()
            os.remove(path_docx)

            if request.method and 'one' in request.POST:
                company = contract.contract_template.company
                generated_date_qr = format_date(contract.date_created, 'd.MM.yy', locale='ru')
                qr = qrcode.QRCode(
                    version=None,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=4,
                    border=3,
                )
                if company == 'ООО "КМС"':
                    if type == 'Основной':
                        qr_kms_basic = qr
                        qr_kms_basic.add_data(
                            'ST00012|Name=ООО "КМС"|'
                            'PersonalAcc=40702810838000108799|'
                            'BankName=ПАО СБЕРБАНК|'
                            'BIC=044525225|'
                            'CorrespAcc=30101810400000000225|'
                            'Purpose=Оплата участия в серии мероприятий для бизнеса "Клуба Первых". '
                            'По Договору оказания услуг ФЛМ-' + id_contract + ' от ' + generated_date_qr + '|'
                            'Sum=1|'
                            'PayeeINN=7725731508|'
                            'KPP=772501001|'
                            'LastName=' + last_name + '|'
                            'FirstName=' + name + '|'
                            'MiddleName=' + sur_name + ''
                        )
                        qr_kms_basic.make(fit=True)
                        path = os.path.join(BASE_DIR, 'upload\\tmp\\' + id_contract + '.png')

                        img = qr_kms_basic.make_image(fill_color="black", back_color="white")
                        bytes_io = BytesIO()
                        img.save(bytes_io, format='png')
                        img_base64 = base64.b64encode(bytes_io.getvalue()).decode()
                        return JsonResponse({'filled_contract': docx_base, 'img_base64': img_base64})
            return render(request, self.template_name, {'form': form})

