# Generated by Django 3.2.12 on 2022-06-08 21:09

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0049_alter_typeofobject_slug'),
        ('region', '0007_auto_20220531_0909'),
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoForType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название страницы')),
                ('image_alt', models.CharField(blank=True, max_length=50, verbose_name='ALT изображения')),
                ('image_title', models.CharField(blank=True, max_length=50, verbose_name='Title для изображения')),
                ('meta_title', models.TextField(blank=True, verbose_name='Мета заголовок')),
                ('meta_description', models.TextField(blank=True, verbose_name='Мета описание')),
                ('content_1', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текстовый блок №1')),
                ('content_2', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текстовый блок №2')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.region', verbose_name='Город')),
                ('type_of_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.typeofobject', verbose_name='Тиж жилья')),
            ],
            options={
                'verbose_name': 'SEO для страницы',
                'verbose_name_plural': 'SEO для статических страниц',
            },
        ),
    ]