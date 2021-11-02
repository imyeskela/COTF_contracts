# Generated by Django 3.2.6 on 2021-11-01 16:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20211101_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticationcode',
            name='date_generated_code',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации кода'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 11, 1, 16, 49, 41, 635848, tzinfo=utc), verbose_name='Дата генерации'),
        ),
    ]
