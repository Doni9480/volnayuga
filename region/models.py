from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.

class Region(models.Model):
    """Направления"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    is_city = models.BooleanField(default=False, verbose_name='Если город, то ставь галочку!')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный курорт')
    image = models.FileField(upload_to='region', verbose_name='Изображение')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родитель', related_name='children')
    description = RichTextField(blank=True, null=True, verbose_name='Описание')
    

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = ' Направления'

    def __str__(self):
        return self.title


class GalleryForRegion(models.Model):
    """Фотографии для региона"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    image = models.ImageField(upload_to='images/region', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Галерея для региона'

