import json

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from services.main_logic import generator_num_contract, get_template_contracts
from services.questionnaire import form_questionnaire, finally_rich, get_sign_img, create_new_code_obj, \
    change_confirmation, change_contract_status, send_sms, send_email_contract_signed, get_time_for_resend_sms
from services.download import get_contract_and_payment, download

from main.models import Contract, ContractTemplate


class ContractTemplateListAndCreateContractMixin:
    """Миксин для отображения всех шаблонов контрактов"""

    queryset = None
    template_name = None
    form_contract = None
    form_contract_template = None
    form_contract_template_change = None

    def get(self, request):
        paginator = Paginator(self.queryset(), 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form_contract_template_change = self.form_contract_template_change()
        return render(request, self.template_name, {'contract_template_list': page_obj,
                                                    'form_contract': self.form_contract,
                                                    'form_contract_template': self.form_contract_template,
                                                    'form_contract_template_change': form_contract_template_change,
                                                    })

    def post(self, request):
        if request.POST:
            form_contract = self.form_contract(request.POST)
            form_contract_template = self.form_contract_template(request.POST, request.FILES)
            print(request.POST)
            if 'create_form' in request.POST:
                paginator = Paginator(self.queryset(), 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                form_contract_template_change = self.form_contract_template_change()

                if form_contract_template.is_valid():
                    if 'check_file' in request.POST:
                        print('AAA')
                        return render(
                            request,
                            self.template_name,
                            {
                                'show_modal': True,
                                'contract_template_list': page_obj,
                                'form_contract': self.form_contract,
                                'form_contract_template': form_contract_template,
                                'form_contract_template_change': form_contract_template_change,
                                'valid': True
                            }
                        )
                    if 'save' in request.POST:
                        form_contract_template = form_contract_template.save(commit=False)
                        form_contract_template.save()
                        return redirect('contract_template_list')
                else:
                    print(form_contract_template.errors)
                    for field_name, field in form_contract_template.fields.items():
                        if field_name in form_contract_template.errors:
                            field.widget.attrs['class'] = 'invalid'

                    return render(
                        request,
                        self.template_name,
                        {
                            'show_modal': True,
                            'contract_template_list': page_obj,
                            'form_contract': self.form_contract,
                            'form_contract_template': form_contract_template,
                            'form_contract_template_change': form_contract_template_change,
                            'valid': False,
                            'template_errors': form_contract_template.errors.get('input_file_name')
                        }
                    )

            elif 'status' in request.POST:
                contract_template = self.queryset().get(pk=request.POST.get('contract_template_pk'))
                form_contract_template_change = self.form_contract_template_change(request.POST, instance=contract_template)
                if form_contract_template_change.is_valid():
                    form_contract_template_change = form_contract_template_change.save(commit=False)
                    form_contract_template_change.save()
                    return redirect('contract_template_list')
        else:
            # Create client
            payload = json.loads(request.body)

            create_contract = payload.get('create_contract')
            identifier = payload.get('identifier')
            amount = payload.get('amount')
            pk = payload.get('pk')

            if create_contract:
                contract_template = ContractTemplate.objects.get(pk=pk)

                contract = Contract(
                    contract_template=contract_template,
                    amount=amount,
                    identifier=identifier,
                    number=generator_num_contract()
                )
                contract.save()

                return JsonResponse({
                    'contract_number': contract.number
                })
            else:
                return JsonResponse({
                    'error': True
                })

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

        download_contract = request.POST.get('download_contract')
        contract_number = request.POST.get('pk')
        status = request.POST.get('status')

        if 'status' in request.POST:
            contract = Contract.objects.get(number=contract_number)
            contract.status = status
            contract.save()

            return redirect('contract_list')

        if download_contract:
            zip_file = download(contract_number=contract_number)
            return zip_file

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
        return render(request, self.template_name, {
            'form': self.form(contract_pk=contract_number),
            'contract': contract,
            'step': 'send_sms'
        })

    def post(self, request, contract_number):
        form = self.form(request.POST, contract_pk=contract_number)

        if 'docx' in request.POST:
            if form.is_valid():
                print('VALID')
                change_confirmation(self, request, contract_number)
                docx_base = form_questionnaire(self, request, contract_number)

                return render(request, self.template_name, {
                    'docx_base': docx_base,
                    'form': form,
                    'step': 'docx'
                })
            else:
                print('INVALID')

                return render(request, self.template_name, {
                    'form': form,
                    'step': 'resend_sms',
                    'show_errors': True
                })

        elif 'qr_code' in request.POST:
            img_base = finally_rich(self, request, contract_number)
            change_contract_status(self)
            send_email_contract_signed(self, request, contract_number)
            return render(request, self.template_name, {
                'img_base': img_base,
                'step': 'qr_code'
            })

        elif 'code' in request.POST:
            if len(form.errors) == 0 or len(form.errors) == 1 and form.errors.get('code'):
                create_new_code_obj(self, request, contract_number)
                send_sms(self, request, contract_number)
                time_sms = get_time_for_resend_sms(self, request, contract_number)

                return render(request, self.template_name, {
                    'form': form,
                    'show_errors': False,
                    'time_sms': time_sms,
                    'step': 'resend_sms'
                })
            else:
                return render(request, self.template_name, {
                    'form': form,
                    'step': 'send_sms'
                })

        return render(request, self.template_name, {'form': form})
