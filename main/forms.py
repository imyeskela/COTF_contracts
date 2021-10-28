from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model
from docxtpl import DocxTemplate

from main.models import ContractTemplate, Contract, AuthenticationCode
from services.questionnaire import get_actual_code


class ContractTemplateCreateForm(forms.ModelForm):
    """Форма для созданания Шаблона Контракта"""

    class Meta:
        model = ContractTemplate
        fields = ['template_of_contract', 'amount', 'status', 'type', 'company']

    def clean(self):
        cleaned_data = super(ContractTemplateCreateForm, self).clean()
        path = self.cleaned_data.get('template_of_contract')
        type_of_contr = str(cleaned_data['type'])

        basic_vars = ['email', 'passport', 'signature', 'full_name',
                      'id', 'generated_date', 'short_name', 'phone']

        renewal_vars = ['sum', 'email', 'passport', 'signature', 'text_sum',
                        'full_name', 'id', 'generated_date', 'short_name', 'phone']

        docx = DocxTemplate(path)
        vars_in_docx = list(docx.undeclared_template_variables)
        if type_of_contr == 'Основной':
            for basic in basic_vars:
                if basic not in vars_in_docx:
                    raise ValidationError('Отсутствуют или внесены неверно переменные <переменные> Пожалуйста, '
                                          'загрузите исправленный документ и выполните проверку повторно')

        elif type_of_contr == 'Продление':
            for renewal in renewal_vars:
                if renewal not in vars_in_docx:
                    raise ValidationError('Отсутствуют или внесены неверно переменные <переменные> Пожалуйста, '
                                          'загрузите исправленный документ и выполните проверку повторно')
        return cleaned_data


class ContractTemplateChangeForm(forms.ModelForm):
    class Meta:
        model = ContractTemplate

        fields = ['status']


class ContractCreateForm(forms.ModelForm):
    """Форма для создания Контракта от Шаблона Контракта"""

    class Meta:
        model = Contract

        fields = ['full_name']
        widgets = {'contract_template': forms.HiddenInput, 'amount': forms.IntegerField}


def valida(value):
    symbols = [".", "-", "'", " "]
    for symbol in symbols:
        if symbol == value[0]:
            raise ValidationError('Недопустимый символ')


class FillingQuestionnaireForm(forms.Form):
    """Форма для подписание Контракта"""
    last_name = forms.CharField(help_text='Фамилия', label='last_name')
    name = forms.CharField(help_text='Имя', label='name')
    sur_name = forms.CharField(help_text='Отчество', required=False, label='sur_name')
    passport = forms.CharField(help_text='Серия и номер паспорта', max_length=11, label='passport')
    email = forms.EmailField(help_text='электронная почта', label='email')
    phone = forms.CharField(help_text='Номер телефона')
    check_box = forms.BooleanField(label='check_box')
    code = forms.IntegerField(required=False)
    # contract_number = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        # use self to store id
        self.form_contract_number = kwargs.pop("contract_pk")
        super(FillingQuestionnaireForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(FillingQuestionnaireForm, self).clean()
        user_code = cleaned_data['code']
        phone = cleaned_data['phone']
        contract = Contract.objects.get(number=self.form_contract_number)
        code = AuthenticationCode.objects.filter(phone=phone, contract=contract, relevance=True).values('code')
        code_n = code[0].get('code')
        if int(user_code) != code_n:
            raise ValidationError('Неправильный код')





