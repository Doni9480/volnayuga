# Generated by Django 3.2.12 on 2022-03-29 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0029_alter_numberprice_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='numberprice',
            options={'verbose_name': 'Цены', 'verbose_name_plural': 'Цены на номера'},
        ),
    ]
