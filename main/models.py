from django.db import models
from django.urls import reverse


class Contract(models.Model):
    """Модель для Контрактов"""

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
    slug = models.SlugField('Url', unique=True, blank=True)
    template_of_contract = models.FileField('Шаблон договора', null=False, upload_to='upload/')
    amount = models.PositiveIntegerField('Сумма', null=True)
    status = models.CharField('Статус', choices=Statuses.choices, default=Statuses.actual, max_length=50)
    type = models.CharField('Тип', choices=Types.choices, null=False, max_length=50)
    # branch = models.ForeignKey('Branch', on_delete=models.CASCADE, blank=True)
    company = models.CharField('Компания', choices=Companies.choices, null=False, max_length=50)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Переопределение метода save для имени и слага"""

        self.name = str(self.type + ' ' + self.company)
        self.slug = self.pk
        super(Contract, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('contract_detail', kwargs={'contract_id': self.pk})


class Branch(models.Model):
    pass