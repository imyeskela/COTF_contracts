from django import forms
from django.core.exceptions import ValidationError
import os
from docxtpl import DocxTemplate
from pathlib import Path, WindowsPath

from main.models import Contract


class ContractCreateForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['template_of_contract', 'amount', 'status', 'type', 'company', 'name']

    def clean(self):
        cleaned_data = super(ContractCreateForm, self).clean()
        path = self.cleaned_data.get('template_of_contract')
        type_of_contr = str(self.cleaned_data['type'])

        basic_vars = ['email', 'passport', 'signature', 'full_name',
                      'id', 'generated_date', 'short_name', 'phone']

        renewal_vars = ['sum', 'email', 'passport', 'signature', 'text_sum',
                        'full_name', 'id', 'generated_date', 'short_name', 'phone']

        docx = DocxTemplate(path)
        vars_in_docx = list(docx.undeclared_template_variables)
        print(vars_in_docx)
        if type_of_contr == 'Основной':
            print('ОСНОВНОЙ')
            for basic in basic_vars:
                if basic not in vars_in_docx:
                    raise ValidationError('IS NOT NIGGER')

        elif type_of_contr == 'Продление':
            print('продление')
            for renewal in renewal_vars:
                if renewal not in vars_in_docx:
                    raise ValidationError('IS NOT NIGGER')
        return cleaned_data


    # def clean_type(self):
    #     type_of_contr = str(self.cleaned_data['type'])
    #     return type_of_contr
    #
    # def clean_template_of_contract(self):
    #     path = self.cleaned_data.get('template_of_contract')
    #     basic_vars = ['sum', 'email', 'passport', 'signature', 'full_name',
    #                   'id', 'generated_date', 'short_name', 'phone']
    #
    #     renewal_vars = ['sum', 'email', 'passport', 'signature', 'text_sum',
    #                     'full_name', 'id', 'generated_date', 'short_name', 'phone']
    #
    #     docx = DocxTemplate(path)
    #     vars_in_docx = list(docx.undeclared_template_variables)
    #     print(vars_in_docx)
    #
    #     if self.clean_type() == 'Основной':
    #         for basic in basic_vars:
    #             if basic not in vars_in_docx:
    #                 raise ValidationError('IS NOT NIGGER')
    #
    #     elif self.clean_type() == 'Продление':
    #         for renewal in renewal_vars:
    #             if renewal not in vars_in_docx:
    #                 raise ValidationError('IS NOT NIGGER')
    #     return path

    # def checking(self):
    #     basic_vars = ['sum', 'email', 'passport', 'signature', 'full_name',
    #                   'id',  'generated_date', 'short_name', 'phone']
    #
    #     renewal_vars = ['sum', 'email', 'passport', 'signature', 'text_sum',
    #                     'full_name', 'id',  'generated_date', 'short_name', 'phone']
    #
    #     docx = DocxTemplate(self.clean_template_of_contract())
    #     vars_in_docx = str(docx.undeclared_template_variables)
    #     print(list(vars_in_docx))
    #
    #     for renewal in renewal_vars:
    #         if renewal != vars_in_docx:
    #             raise ValidationError('IS NOT NIGGER')
    #     return vars_in_docx

    # def clean(self):
    #     renewal_vars = ['sum', 'email', 'passport', 'signature', 'text_sum',
    #             'full_name', 'id',  'generated_date', 'short_name', 'phone']
    #     basic_vars = ['sum', 'email', 'passport', 'signature',
    #             'full_name', 'id',  'generated_date', 'short_name', 'phone']
    #     path = str(self.clean_template_of_contract())
    #     typ = str(self.cleaned_data['type'])
    #     print(path)
    #     print(typ)
    #     doc = DocxTemplate(path)
    #     vars_in_docx = list(doc.undeclared_template_variables)
    #     print(vars_in_docx)
    #     print(self.cleaned_data)
    #     print(d)
    #     print(d)
    #     if d == 'Основной':
    #         for var in basic_vars:
    #             if var == vars_in_docx:
    #                 pass
    #             else:
    #                 raise ValidationError('IS NOT NIGGER')
    #     elif d == 'Продление':
    #         for var in renewal_vars:
    #             if var == vars_in_docx:
    #                 pass
    #             else:
    #                 raise ValidationError('IS NOT NIGGER')
    #     else:
    #         pass
    #     return path, typ