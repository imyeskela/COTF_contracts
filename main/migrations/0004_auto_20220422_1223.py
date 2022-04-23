# Generated by Django 3.2.6 on 2022-04-22 08:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220422_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticationcode',
            name='date_generated_code',
            field=models.CharField(default=1650615838.5296102, max_length=1000, verbose_name='Секунды генерации кода'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 4, 22, 8, 23, 58, 526659, tzinfo=utc), verbose_name='Дата генерации'),
        ),
    ]
