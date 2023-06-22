from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class StaticData(models.Model):
    """Static data on site"""
    logo = models.ImageField(blank=True, upload_to='core/images', verbose_name='Логотип')
    logo_footer = models.ImageField(blank=True, upload_to='core/images', verbose_name='Логотип в подвале')
    banner = models.ImageField(blank=True, upload_to='core/images', verbose_name='Баннер')
    phone = models.CharField(max_length=15,blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Статические данные сайта'
        verbose_name_plural = 'Статические данные сайта'

    def __str__(self):
        return 'Логотипы и контактная информация'
