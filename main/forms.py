from django import forms
from django.core.exceptions import ValidationError
from docxtpl import DocxTemplate

from main.models import ContractTemplate, Contract


class ContractTemplateCreateForm(forms.ModelForm):

    class Meta:
        model = ContractTemplate
        fields = ['template_of_contract', 'amount', 'status', 'type', 'company', 'name']

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
                    raise ValidationError('IS NOT NIGGER')

        elif type_of_contr == 'Продление':
            for renewal in renewal_vars:
                if renewal not in vars_in_docx:
                    raise ValidationError('IS NOT NIGGER')
        return cleaned_data


class ContractCreateForm(forms.ModelForm):

    class Meta:
        model = Contract

        fields = ['full_name']
        widgets = {'contract_template': forms.HiddenInput, 'amount_bitch': forms.IntegerField}


class FillingQuestionnaireForm(forms.Form):
    last_name = forms.CharField(help_text='Фамилия')
    name = forms.CharField(help_text='Имя')
    sur_name = forms.CharField(help_text='Отчество', required=False)
    passport = forms.CharField(help_text='Серия и номер паспорта')
    email = forms.EmailField(help_text='электронная почта')
    phone = forms.IntegerField(help_text='Номер телефона')



