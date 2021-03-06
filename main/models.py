import time

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from babel.dates import format_date


cities = [
    ('Москва', 'Москва'),
    ('Санкт-Петербург', 'Санкт-Петербург')
]


def check_format_of_file(value):
    """Проверка формата на docx"""

    if not value.name.endswith('.docx'):
        raise ValidationError(u'Выберите файл с форматом .docx')


def check_format_of_payment(value):
    """Проверка формата на xlsx"""

    if not value.name.endswith('.xlsx'):
        raise ValidationError(u'Выберите файл с форматом .xlsx')


def check_format_signed_contract(value):
    """Проверка формата на pdf"""

    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Выберите файл с форматом .pdf')


def _generator_num_contract():
    """Генератор номера договора"""

    try:
        contract = Contract.objects.last()
        contract_num = getattr(contract, 'number')
        return contract_num
    except AttributeError:
        return 24546799


class ContractTemplate(models.Model):
    """Модель для Шаблонов контркта"""

    class Statuses(models.TextChoices):
        """Модель выборы Статуса"""

        actual = 'Актуально', 'Актуально'
        outdated = 'Устарело', 'Устарело'

    class Types(models.TextChoices):
        """Модель выборы Типов"""

        basic = 'Основной', 'Основной'
        renewal = 'Продление', 'Продление'

    class Companies(models.TextChoices):
        """Модель выборы Компании"""

        CMS = 'ООО "КМС"', ('ООО "КМС"')
        DC = 'ООО "ДЕЛОВОЙ КЛУБ"', ('ООО "ДЕЛОВОЙ КЛУБ"')

    city = models.CharField('Город', choices=cities, null=True, max_length=50, default='Москва')

    name = models.CharField('Название', null=False, max_length=50, blank=True)
    template_of_contract = models.FileField('Шаблон договора', null=False, upload_to='upload/', validators=[check_format_of_file])
    amount = models.PositiveIntegerField('Сумма', null=True, default=None)
    status = models.CharField('Статус', choices=Statuses.choices, default=Statuses.actual, max_length=100)
    type = models.CharField('Тип', choices=Types.choices, null=False, max_length=50, default='Основной')
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

        directed = 'Направлен', 'Направлен'
        signed = 'Подписан', 'Подписан'
        canceled = 'Отменен', 'Отменен'
        refusal = 'Отказ', 'Отказ'

    number = models.PositiveBigIntegerField('Номер договора', default=24546799, null=False)
    contract_template = models.ForeignKey(ContractTemplate, on_delete=models.CASCADE, null=False)
    payment = models.FileField('Счет на оплату', null=True, upload_to='payment/',
                               validators=[check_format_of_payment], blank=True)
    signed_contract = models.FileField('Подписанный договор', upload_to='signed_contract/',
                                       null=True)
    date_created = models.DateField('Дата генерации', default=timezone.now())
    date_signed = models.DateField('Дата подписания', blank=True, null=True)
    status = models.CharField('Статус', choices=Statuses.choices, default=Statuses.directed, max_length=50)
    full_name = models.CharField('ФИО', null=False, max_length=300)
    amount = models.PositiveIntegerField('Сумма', null=True,max_length=300)
    name = models.CharField('Название', max_length=400, null=False)
    series_passport = models.PositiveIntegerField('Серия паспорт', max_length=4, blank=True, null=True)
    num_passport = models.PositiveIntegerField('Номер паспорт', max_length=6, blank=True, null=True)
    email = models.EmailField('Почта', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    identifier = models.CharField('Индетификатор', max_length=50, blank=True, null=True, default='Данных нет')

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def save(self, *args, **kwargs):
        """Переопределение метода save для имени и номера договора"""

        self.name = str(self.contract_template.type + ' ' + self.full_name + ' ' +
                        self.contract_template.company + ' ' + format_date(self.date_created, 'd MMMM yyyy', locale='ru'))
        super(Contract, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('contract_detail', kwargs={'contract_number': str(self.number)})

    def __str__(self):
        return str(self.number)


class AuthenticationCode(models.Model):
    code = models.PositiveIntegerField('Код', null=False, unique=True, max_length=5)
    number_of_attempts = models.PositiveSmallIntegerField('Количество попыток ввода', default=0)
    date_generated_code = models.CharField('Секунды генерации кода', default=time.time(), max_length=1000)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)
    phone = models.CharField('Номер телефона', max_length=12)
    confirmation = models.BooleanField('Флаг подтверждения', default=False)
    relevance = models.BooleanField('Флаг актуальности')

    class Meta:
        verbose_name = 'Код аутентификации'
        verbose_name_plural = 'Коды аутентификации'

    def __str__(self):
        return str(self.code)
