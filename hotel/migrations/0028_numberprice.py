# Generated by Django 3.2.12 on 2022-03-29 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0027_auto_20220328_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(verbose_name='Начало периода')),
                ('finish', models.DateField(verbose_name='Конец периода')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.number', verbose_name='Номер')),
            ],
            options={
                'verbose_name': 'Цену',
                'verbose_name_plural': 'Цены на номера',
            },
        ),
    ]
