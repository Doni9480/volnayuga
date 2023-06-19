# Generated by Django 3.2.12 on 2023-06-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0013_remove_seopage_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='seopage',
            name='address',
            field=models.TextField(blank=True, verbose_name='Адрес (Страница контакты)'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='email_1',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта 1 (Страница контакты)'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='email_2',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта 2 (Страница контакты)'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='phone_1',
            field=models.CharField(blank=True, max_length=15, verbose_name='Телефон 1 (Страница контакты)'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='phone_2',
            field=models.CharField(blank=True, max_length=15, verbose_name='Телефон 2 (Страница контакты)'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='requisite_1',
            field=models.CharField(blank=True, max_length=100, verbose_name='Реквизит 1 (Страница контакты)'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='requisite_2',
            field=models.CharField(blank=True, max_length=100, verbose_name='Реквизит 2 (Страница контакты)'),
        ),
    ]
