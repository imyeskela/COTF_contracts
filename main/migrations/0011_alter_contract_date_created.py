# Generated by Django 3.2.6 on 2021-10-05 14:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20211005_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 10, 5, 14, 42, 19, 134341, tzinfo=utc), verbose_name='Дата генерации'),
        ),
    ]