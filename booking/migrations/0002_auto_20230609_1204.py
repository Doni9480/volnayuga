# Generated by Django 3.2.12 on 2023-06-09 12:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelbooking',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 9, 12, 4, 26, 581899, tzinfo=utc), verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='hotelbooking',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 9, 12, 4, 26, 581883, tzinfo=utc), verbose_name='Дата начала'),
        ),
    ]
