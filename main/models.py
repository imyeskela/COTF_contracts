import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone


def check_format_of_file(value):
    if not value.name.endswith('.docx'):
        raise ValidationError(u'Выберите файл с форматом .docx')


def check_format_of_payment(value):
    if not value.name.endswith('.xlsx'):
        raise ValidationError(u'Выберите файл с форматом .xlsx')


def check_format_signed_contract(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Выберите файл с форматом .pdf')


class ContractTemplate(models.Model):
    """Модель для Шаблонов контркта"""

    class Statuses(models.TextChoices):
        """Модель выборы Статуса"""

        actual = 'Актуально'
        outdated = 'Устарело'

    class Types(models.TextChoices):
        """Модель выборы Типов"""

        basic = 'Основной'
        renewal = 'Продление'

    class Companies(models.TextChoices):
        """Модель выборы Компании"""

        CMS = 'ООО "Комьюнити Менеджмент Солюшнз"'
        DC = 'ООО "ДЕЛОВОЙ КЛУБ"'

    name = models.CharField('Название', null=False, max_length=50, blank=True)
    template_of_contract = models.FileField('Шаблон договора', null=False, upload_to='upload/', validators=[check_format_of_file])
    amount = models.PositiveIntegerField('Сумма', null=True)
    status = models.CharField('Статус', choices=Statuses.choices, default=Statuses.actual, max_length=50)
    type = models.CharField('Тип', choices=Types.choices, null=False, max_length=50)
    # branch = models.ForeignKey('Branch', on_delete=models.CASCADE, blank=True)
    company = models.CharField('Компания', choices=Companies.choices, null=False, max_length=50)

    class Meta:
        verbose_name = 'Шаблон контракта'
        verbose_name_plural = 'Шаблоны контрактов'

    def save(self, *args, **kwargs):
        """Переопределение метода save для имени и слага"""

        self.name = str(self.type + ' ' + self.company)
        super(ContractTemplate, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contract(models.Model):
    """Модель для Контркта"""

    class Statuses(models.TextChoices):
        """Модель выборы Статуса"""

        directed = 'Направлен'
        signed = 'Подписан'
        canceled = 'Отменен'
        refusal = 'Отказ'

    number = models.PositiveBigIntegerField('Номер договора', default=str(24546799), null=False)
    contract_template = models.ForeignKey(ContractTemplate, on_delete=models.CASCADE, null=False)
    payment = models.FileField('Счет на оплату', null=True, upload_to='payment/',
                               validators=[check_format_of_payment])
    signed_contract = models.FileField('Подписанный договор', upload_to='signed_contract/',
                                       null=True, validators=[check_format_signed_contract])
    date_created = models.DateField('Дата генерации', auto_now_add=True)
    date_signed = models.DateField('Дата подписания', blank=True, null=True)
    status = models.CharField('Статус', choices=Statuses.choices, default=Statuses.directed, max_length=50)
    full_name = models.CharField('ФИО', null=False, max_length=150)
    amount = models.PositiveIntegerField('Сумма', null=True)
    name = models.CharField('Название', max_length=200, null=False)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def save(self, *args, **kwargs):
        """Переопределение метода save для имени и слага"""

        self.name = str(self.full_name + '' + str(self.date_created))
        super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return self.number


class Branch(models.Model):
    pass