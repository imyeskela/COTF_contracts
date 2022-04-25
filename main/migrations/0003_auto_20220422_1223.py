# Generated by Django 3.2.6 on 2022-04-22 08:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220415_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracttemplate',
            name='city',
            field=models.CharField(max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='authenticationcode',
            name='date_generated_code',
            field=models.CharField(default=1650615824.487243, max_length=1000, verbose_name='Секунды генерации кода'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 4, 22, 8, 23, 44, 486246, tzinfo=utc), verbose_name='Дата генерации'),
        ),
        migrations.AlterField(
            model_name='contracttemplate',
            name='type',
            field=models.CharField(choices=[('Основной', 'Основной'), ('Продление', 'Продление')], default='Основной', max_length=50, verbose_name='Тип'),
        ),
    ]