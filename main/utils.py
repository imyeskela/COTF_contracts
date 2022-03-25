from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from services.main_logic import generator_num_contract, get_template_contracts
from services.questionnaire import form_questionnaire, finally_rich, get_sign_img, create_new_code_obj, \
    change_confirmation, change_contract_status, get_time_for_resend_sms, send_sms, send_email_contract_signed
from services.download import get_contract_and_payment, download


class ContractTemplateListAndCreateContractMixin:
    """Миксин для отображения всех шаблонов контрактов"""

    queryset = None
    template_name = None
    form_contract = None
    form_contract_template = None
    form_contract_template_change = None

    def get(self, request):
        paginator = Paginator(self.queryset, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        queryset = self.queryset
        form_contract_template_change = self.form_contract_template_change()
        return render(request, self.template_name, {'contract_template_list': page_obj,
                                                    'form_contract': self.form_contract,
                                                    'form_contract_template': self.form_contract_template,
                                                    'form_contract_template_change': form_contract_template_change,
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
                form_contract.save()
                return redirect('contract_list')
            else:
                return render(request, self.template_name, {'form_contract': form_contract,
                                                            'form_contract_template': form_contract_template
                                                            })

        elif 'create_form' in request.POST:
            paginator = Paginator(self.queryset, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            form_contract_template_change = self.form_contract_template_change()

            print(form_contract_template.is_valid())
            print(form_contract_template.errors)
            if form_contract_template.is_valid():
                form_contract_template = form_contract_template.save(commit=False)
                form_contract_template.save()
                return redirect('contract_template_list')
            else:
                return render(
                    request,
                    self.template_name,
                    {
                        'show_modal': True,
                        'contract_template_list': page_obj,
                        'form_contract': self.form_contract,
                        'form_contract_template': form_contract_template,
                        'form_contract_template_change': form_contract_template_change,
                    }
                )

        elif 'status' in request.POST:
            contract_template = self.queryset.get(pk=request.POST.get('contract_template_pk'))
            form_contract_template_change = self.form_contract_template_change(request.POST, instance=contract_template)
            if form_contract_template_change.is_valid():
                form_contract_template_change = form_contract_template_change.save(commit=False)
                form_contract_template_change.save()
                return redirect('contract_template_list')

        return render(request, self.template_name, {
            'form_contract': form_contract,
        })


class AdministrationMixin:
    template_name = None

    def get(self, request):
        return render(
            request,
            self.template_name,
            {}
        )


class ContractListMixin:
    """Миксин для отображения всех контрактов"""

    queryset = None
    template_name = None
    form_contract_template = None
    form_contract = None

    def get(self, request):
        paginator = Paginator(self.queryset(), 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        template_name = self.template_name
        # print(request.POST)

        return render(request, template_name, {'contract_list': page_obj,
                                               'form_contract_template': self.form_contract_template,
                                               'form_contract': self.form_contract,

                                               })

    def post(self, request):
        form_contract_template = self.form_contract_template(request.POST, request.FILES)
        # form_contract = self.form_contract(request.POST)
        if 'create_contract_template' in request.POST:
            if form_contract_template.is_valid():
                form_contract_template = form_contract_template.save(commit=False)
                form_contract_template.save()
                return redirect('contract_template_list')
            else:
                return render(request, self.template_name,
                              {'form_contract_template': form_contract_template})

        # elif 'download_contract' in request.POST:
        #     contract_number = request.POST.get('contract_number')
        #     zip_file = download(contract_number=contract_number)
        #
        #     return render(request, self.template_name,
        #                   {'response': zip_file})

        return render(request, self.template_name,
                      {'form_contract_template': form_contract_template})


class FillingQuestionnaireMixin:
    """Миксин для формы анкета"""

    form = None
    contract = None
    template_name = None

    def get(self, request, contract_number):
        contract = self.contract()
        if contract.status == 'Подписан':
            return HttpResponseNotFound('404')
        return render(request, self.template_name, {'form': self.form(contract_pk=contract_number), 'contract': contract})

    def post(self, request, contract_number):
        form = self.form(request.POST, contract_pk=contract_number)

        if 'docx' in request.POST:
            if form.is_valid():
                change_confirmation(self, request, contract_number)
                docx_base = form_questionnaire(self, request, contract_number)
                return render(request, self.template_name, {'docx_base': docx_base, 'form': form})

        elif 'qr_code' in request.POST:
            img_base = finally_rich(self, request, contract_number)
            get_sign_img(self, request, contract_number)
            change_contract_status(self)
            send_email_contract_signed(self, request, contract_number)
            return render(request, self.template_name, {'img_base': img_base})
        elif 'code' in request.POST:
            create_new_code_obj(self, request, contract_number)
            send_sms(self, request, contract_number)
            time_sms = get_time_for_resend_sms(self, request, contract_number)
            return render(request, self.template_name, {'form': form, 'time_sms': time_sms})
        return render(request, self.template_name, {'form': form})



