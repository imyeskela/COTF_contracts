# Generated by Django 3.2.6 on 2021-09-14 00:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210913_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 9, 14, 0, 56, 19, 580505, tzinfo=utc), verbose_name='Дата генерации'),
        ),
        migrations.AlterField(
            model_name='contracttemplate',
            name='company',
            field=models.CharField(choices=[('ООО "КМС"', 'ООО "КМС"'), ('ООО "ДЕЛОВОЙ КЛУБ"', 'ООО "ДЕЛОВОЙ КЛУБ"')], max_length=50, verbose_name='Компания'),
        ),
    ]