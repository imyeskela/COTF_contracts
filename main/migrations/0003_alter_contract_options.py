# Generated by Django 3.2.6 on 2021-09-01 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210901_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ['id'], 'verbose_name': 'Контракт', 'verbose_name_plural': 'Контракты'},
        ),
    ]
