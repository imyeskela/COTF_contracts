# Generated by Django 3.2.6 on 2022-04-15 14:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='Название')),
                ('template_of_contract', models.FileField(upload_to='upload/', validators=[main.models.check_format_of_file], verbose_name='Шаблон договора')),
                ('amount', models.PositiveIntegerField(null=True, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('Актуально', 'Актуально'), ('Устарело', 'Устарело')], default='Актуально', max_length=100, verbose_name='Статус')),
                ('type', models.CharField(choices=[('Основной', 'Основной'), ('Продление', 'Продление')], max_length=50, verbose_name='Тип')),
                ('company', models.CharField(choices=[('ООО "КМС"', 'ООО "КМС"'), ('ООО "ДЕЛОВОЙ КЛУБ"', 'ООО "ДЕЛОВОЙ КЛУБ"')], max_length=50, verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Шаблон контракта',
                'verbose_name_plural': 'Шаблоны контрактов',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveBigIntegerField(default=24546799, verbose_name='Номер договора')),
                ('payment', models.FileField(blank=True, null=True, upload_to='payment/', validators=[main.models.check_format_of_payment], verbose_name='Счет на оплату')),
                ('signed_contract', models.FileField(null=True, upload_to='signed_contract/', verbose_name='Подписанный договор')),
                ('date_created', models.DateField(default=datetime.datetime(2022, 4, 15, 14, 37, 23, 639331, tzinfo=utc), verbose_name='Дата генерации')),
                ('date_signed', models.DateField(blank=True, null=True, verbose_name='Дата подписания')),
                ('status', models.CharField(choices=[('Направлен', 'Направлен'), ('Подписан', 'Подписан'), ('Отменен', 'Отменен'), ('Отказ', 'Отказ')], default='Направлен', max_length=50, verbose_name='Статус')),
                ('full_name', models.CharField(max_length=300, verbose_name='ФИО')),
                ('amount', models.PositiveIntegerField(max_length=300, null=True, verbose_name='Сумма')),
                ('name', models.CharField(max_length=400, verbose_name='Название')),
                ('series_passport', models.PositiveIntegerField(blank=True, max_length=4, null=True, verbose_name='Серия паспорт')),
                ('num_passport', models.PositiveIntegerField(blank=True, max_length=6, null=True, verbose_name='Номер паспорт')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
                ('identifier', models.CharField(blank=True, default='Данных нет', max_length=50, null=True, verbose_name='Индетификатор')),
                ('contract_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.contracttemplate')),
            ],
            options={
                'verbose_name': 'Контракт',
                'verbose_name_plural': 'Контракты',
            },
        ),
        migrations.CreateModel(
            name='AuthenticationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(max_length=5, unique=True, verbose_name='Код')),
                ('number_of_attempts', models.PositiveSmallIntegerField(default=0, verbose_name='Количество попыток ввода')),
                ('date_generated_code', models.TimeField(default=1650033443.6403317, verbose_name='Секунды генерации кода')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('confirmation', models.BooleanField(default=False, verbose_name='Флаг подтверждения')),
                ('relevance', models.BooleanField(verbose_name='Флаг актуальности')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.contract')),
            ],
            options={
                'verbose_name': 'Код аутентификации',
                'verbose_name_plural': 'Коды аутентификации',
            },
        ),
    ]
