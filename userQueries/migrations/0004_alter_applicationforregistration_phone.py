# Generated by Django 3.2.12 on 2023-06-21 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userQueries', '0003_auto_20230622_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationforregistration',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон'),
        ),
    ]
