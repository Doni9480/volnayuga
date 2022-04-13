# Generated by Django 3.2.12 on 2022-03-11 11:09

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Пляж',
                'verbose_name_plural': 'Пляжи',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(default='1', unique=True, verbose_name='URL')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('remoteness', models.IntegerField(blank=True, null=True, verbose_name='Удаленность от пляжа')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='Описание')),
                ('video', models.URLField(blank=True, verbose_name='Видео объекта')),
                ('prepayment', models.CharField(blank=True, max_length=10, verbose_name='Предоплата')),
                ('free_cancel', models.CharField(blank=True, max_length=100, verbose_name='Условия бесплатной отмены брони')),
                ('early_booking_discount', models.IntegerField(blank=True, null=True, verbose_name='Скидка на раннее бронирование')),
                ('requisites', models.TextField(blank=True, verbose_name='Реквизиты')),
                ('prepayments_term', models.BooleanField(default=0, verbose_name='Без предоплаты')),
                ('minimum', models.IntegerField(blank=True, verbose_name='Минимальный срок проживания в сутках')),
                ('chek_in', models.TimeField(blank=True, verbose_name='Время заселения')),
                ('chek_out', models.TimeField(blank=True, verbose_name='Время выезда')),
                ('pets', models.BooleanField(default=0, verbose_name='Животные')),
                ('child', models.BooleanField(default=0, verbose_name='Дети')),
                ('another_rules', models.TextField(blank=True, verbose_name='Другие правила')),
                ('beach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.beach', verbose_name='Пляж')),
                ('city', models.ForeignKey(limit_choices_to={'is_city': True}, on_delete=django.db.models.deletion.CASCADE, to='region.region', verbose_name='Город')),
            ],
            options={
                'verbose_name': ' Обьект размещения',
                'verbose_name_plural': ' Гостиницы',
            },
        ),
        migrations.CreateModel(
            name='Hotel_contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('photo', models.FileField(upload_to='images/contacts', verbose_name='Фотография')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('skype', models.BooleanField(default=0)),
                ('whatsapp', models.BooleanField(default=0)),
                ('telegram', models.BooleanField(default=0)),
                ('viber', models.BooleanField(default=0)),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты объектов размещения',
            },
        ),
        migrations.CreateModel(
            name='Hotel_option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Опцию',
                'verbose_name_plural': ' Опции для гостиниц',
            },
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('room_number', models.IntegerField(blank=True, null=True, verbose_name='Количество комнат')),
                ('sleep_place', models.IntegerField(blank=True, null=True, verbose_name='Количество спальных мест')),
                ('room_square', models.IntegerField(blank=True, null=True, verbose_name='Площадь комнаты')),
                ('additional_palces', models.IntegerField(blank=True, null=True, verbose_name='Дополнительные места')),
                ('furniture', models.TextField(blank=True, verbose_name='Мебель')),
                ('hotel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel', verbose_name='Отель')),
            ],
            options={
                'verbose_name': ' Номер',
                'verbose_name_plural': ' Номера',
            },
        ),
        migrations.CreateModel(
            name='Number_option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Опцию',
                'verbose_name_plural': ' Опции для номеров',
            },
        ),
        migrations.CreateModel(
            name='Type_of_Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': ' Типы объектов размещения',
            },
        ),
        migrations.CreateModel(
            name='Photo_on_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/hotel_photo', verbose_name='Изображение')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name': 'Фотографию',
                'verbose_name_plural': 'Фотографии объекта для страницы объекта',
            },
        ),
        migrations.CreateModel(
            name='Photo_in_filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/hotel_photo_thumb', verbose_name='Изображение')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name': 'Фотографию',
                'verbose_name_plural': 'Фотографии объекта для страниц фильтрации',
            },
        ),
        migrations.CreateModel(
            name='Number_photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/numbers', verbose_name='Изображение')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.number')),
            ],
        ),
        migrations.AddField(
            model_name='number',
            name='options',
            field=models.ManyToManyField(to='hotel.Number_option', verbose_name='Опции'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel_contact', verbose_name='Контакты'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='object_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.type_of_object', verbose_name='Тип объекта'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='options',
            field=models.ManyToManyField(to='hotel.Hotel_option', verbose_name='Опции'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]