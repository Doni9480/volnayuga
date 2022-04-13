# Generated by Django 3.2.12 on 2022-04-05 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0033_hotel_premium'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoteloption',
            name='category',
            field=models.CharField(choices=[('food', 'Питание'), ('service', 'Удобства и услуги'), ('booking', 'Условия бронирования')], default='food', max_length=50, verbose_name='Категория'),
        ),
    ]