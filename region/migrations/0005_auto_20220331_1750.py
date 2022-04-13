# Generated by Django 3.2.12 on 2022-03-31 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0004_region_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='meta_description',
            field=models.TextField(blank=True, verbose_name='Мета описание'),
        ),
        migrations.AddField(
            model_name='region',
            name='meta_title',
            field=models.CharField(blank=True, max_length=100, verbose_name='Мета заголовок'),
        ),
    ]