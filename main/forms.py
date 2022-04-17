import random
from collections import defaultdict

from django.utils.safestring import mark_safe
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model
from docxtpl import DocxTemplate

from main.models import ContractTemplate, Contract, AuthenticationCode

from services.ordering import get_ordered_contracts
from services.questionnaire import get_actual_code
from services.validation import are_there_ru_words, are_there_special_symbols, are_there_nums, is_valid_, is_int


class ContractTemplateCreateForm(forms.ModelForm):
    """Форма для созданания Шаблона Контракта"""
    create_form = forms.BooleanField(widget=forms.HiddenInput, required=False)
    check_file = forms.BooleanField(widget=forms.HiddenInput, required=False)

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

        try:
            docx = DocxTemplate(path)
        except Exception as e:
            print(e)
            # Откуда берется сообщение об ошибке, если message is required
            raise ValidationError('ERROR')

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


# class ContractTemplateChangeForm(forms.Form):
#     status = forms.ChoiceField(choices=('Акутально', 'Устарело'))


class ContractTemplateChangeForm(forms.ModelForm):
    contract_template_pk = forms.IntegerField(widget=forms.HiddenInput, label='contract_template_pk')

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


class ContractListForm(forms.Form):
    # class Meta:
    #     widgets = {'contract_number': forms.HiddenInput}
    contract_number = forms.IntegerField(widget=forms.HiddenInput, label='contract_number')


class FillingQuestionnaireForm(forms.Form):
    """Форма для подписание Контракта"""
    last_name = forms.CharField(
        label='Фамилия*',
        required=True,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фамилия'
            }
        )
    )
    name = forms.CharField(
        label='Имя*',
        required=True,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя'
            }
        )
    )
    sur_name = forms.CharField(
        required=False,
        label='Отчество',
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Отчество'
            }
        )
    )
    series_passport = forms.CharField(
        max_length=4,
        required=True,
        label='Серия паспорта*',
        widget=forms.TextInput(
            attrs={
                'placeholder': '0000'
            }
        )
    )
    num_passport = forms.CharField(
        max_length=6,
        required=True,
        label='Номер паспорта*',
        widget=forms.TextInput(
            attrs={
                'placeholder': '000000'
            }
        )
    )
    email = forms.EmailField(
        label='Email*',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Почта'
            }
        )
    )
    phone = forms.CharField(
        label='Мобильный телефона*',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Мобильный телефона'
            }
        )
    )
    check_box = forms.BooleanField(label='check_box')
    code = forms.IntegerField(required=False, initial=0)

    def __init__(self, *args, **kwargs):
        # use self to store id
        self.form_contract_number = kwargs.pop("contract_pk")
        super(FillingQuestionnaireForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(FillingQuestionnaireForm, self).clean()

        name = cleaned_data.get('name')
        if is_valid_(name) is False:
            self.add_error('name', 'Укажите корректное имя')

        last_name = cleaned_data.get('last_name')
        if is_valid_(last_name) is False:
            self.add_error('last_name', 'Укажите корректную фамилию')

        sur_name = cleaned_data.get('sur_name')
        if is_valid_(sur_name) is False:
            self.add_error('sur_name', 'Укажите корректное отчество')

        series_passport = cleaned_data.get('series_passport')
        if is_int(series_passport) is False:
            self.add_error('series_passport', 'Некорректная серия')
        # if are_there_ru_words(series_passport):
        #     self.add_error('series_passport', 'Некорректная серия')

        num_passport = cleaned_data.get('num_passport')
        if is_int(num_passport) is False:
            self.add_error('num_passport', 'Некорректный номер')

        check_box = cleaned_data.get('check_box')
        if not check_box:
            self.add_error('check_box', 'Подтвердите согласие на обработку персональных данных')

        phone = cleaned_data['phone']
        if is_int(phone[2:]) is False:
            self.add_error('phone', 'Укажите корректный номер телефона')

        contract = Contract.objects.get(number=self.form_contract_number)
        try:
            codes = AuthenticationCode.objects.get(phone=phone, contract=contract, relevance=True)
        except:
            codes = None

        print(cleaned_data.keys())

<<<<<<< HEAD
        user_code = cleaned_data.get('code')

=======
        # if 'code' in cleaned_data.keys():
        #     pass

        user_code = cleaned_data.get('code')
        print(user_code)
>>>>>>> ac45ae5ddbe83fa098e4f6ac2fe7e50ed73528d7
        if str(user_code) != str(codes):
            self.add_error('code', 'Неверный код')
