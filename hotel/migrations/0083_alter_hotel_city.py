# Generated by Django 3.2.12 on 2023-06-05 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0009_remove_region_description'),
        ('hotel', '0082_delete_hotelreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(limit_choices_to={'is_city': True}, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='region.region', verbose_name='Город'),
        ),
    ]