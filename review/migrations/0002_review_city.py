# Generated by Django 3.2.12 on 2023-05-08 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='city',
            field=models.CharField(blank=True, max_length=200, verbose_name='Город'),
        ),
    ]
