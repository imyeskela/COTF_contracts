# Generated by Django 3.2.6 on 2021-11-21 17:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 11, 21, 17, 26, 59, 487511, tzinfo=utc), verbose_name='Дата генерации'),
        ),
    ]
