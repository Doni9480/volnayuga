# Generated by Django 3.2.12 on 2022-03-12 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_auto_20220312_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel_contact', verbose_name='Контакты'),
        ),
    ]