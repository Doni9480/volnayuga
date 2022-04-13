# Generated by Django 3.2.12 on 2022-04-05 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0034_hoteloption_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distancetime',
            name='hotel',
            field=models.ManyToManyField(blank=True, to='hotel.Hotel', verbose_name='Гостиница'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='options',
            field=models.ManyToManyField(blank=True, to='hotel.HotelOption', verbose_name='Опции'),
        ),
        migrations.AlterField(
            model_name='number',
            name='options',
            field=models.ManyToManyField(blank=True, to='hotel.NumberOption', verbose_name='Опции'),
        ),
    ]
