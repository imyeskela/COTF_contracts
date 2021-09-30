from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model
from docxtpl import DocxTemplate

from main.models import ContractTemplate, Contract


class ContractTemplateCreateForm(forms.ModelForm):

    class Meta:
        model = ContractTemplate
        fields = ['template_of_contract', 'amount', 'status', 'type', 'company']

    def clean(self):
        cleaned_data = super(ContractTemplateCreateForm, self).clean()
        path = self.cleaned_data.get('template_of_contract')
        type_of_contr = str(self.cleaned_data['type'])

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
        return self.cleaned_data


class ContractCreateForm(forms.ModelForm):

    class Meta:
        model = Contract

        fields = ['full_name']
        widgets = {'contract_template': forms.HiddenInput, 'amount': forms.IntegerField}


def valida(value):
    symbols = [".", "-", "'", " "]
    print(value)
    for symbol in symbols:
        if symbol == value[0]:
            raise ValidationError('Недопустимый символ')


class FillingQuestionnaireForm(forms.Form):
    last_name = forms.CharField(help_text='Фамилия', label='last_name')
    name = forms.CharField(help_text='Имя', label='name')
    sur_name = forms.CharField(help_text='Отчество', required=False, label='sur_name')
    passport = forms.CharField(help_text='Серия и номер паспорта', max_length=11, label='passport')
    email = forms.EmailField(help_text='электронная почта', label='email')
    phone = forms.CharField(help_text='Номер телефона', label='phone')
    check_box = forms.BooleanField(label='check_box')




