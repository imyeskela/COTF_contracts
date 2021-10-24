# Generated by Django 3.2.6 on 2021-10-24 16:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_contract_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(unique=True, verbose_name='Код')),
                ('number_of_attempts', models.PositiveSmallIntegerField(default=0, verbose_name='Количество попыток ввода')),
                ('generated_code', models.DateField(default=datetime.datetime(2021, 10, 24, 16, 22, 21, 751509, tzinfo=utc), verbose_name='Дата генерации кода')),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='Номер телефона')),
                ('confirmation', models.BooleanField(default=False, verbose_name='Флаг подтверждения')),
                ('relevance', models.BooleanField(verbose_name='Флаг актуальности')),
            ],
            options={
                'verbose_name': 'Код аутентификации',
                'verbose_name_plural': 'Коды аутентификации',
            },
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 10, 24, 16, 22, 21, 750508, tzinfo=utc), verbose_name='Дата генерации'),
        ),
        migrations.AddField(
            model_name='authenticationcode',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.contract'),
        ),
    ]
