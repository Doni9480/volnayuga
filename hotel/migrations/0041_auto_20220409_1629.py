# Generated by Django 3.2.12 on 2022-04-09 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0040_auto_20220409_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='numberphoto',
            options={'verbose_name': 'Фотографии номера', 'verbose_name_plural': 'Фотографии номера'},
        ),
        migrations.RemoveField(
            model_name='numberprice',
            name='dop_place',
        ),
    ]
