# Generated by Django 3.2.6 on 2021-10-23 21:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20211006_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 10, 23, 21, 9, 19, 283876, tzinfo=utc), verbose_name='Дата генерации'),
        ),
    ]
