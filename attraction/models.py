from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class AttractionCategory(models.Model):
    """Категория достопримечательности"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория достопримечательности'
        verbose_name_plural = 'Категории достопримечательностей'


class Attraction(models.Model):
    """Достопримечательности регионов"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    category = models.ForeignKey(AttractionCategory, on_delete=models.CASCADE, verbose_name='Категория')
    content = RichTextField(verbose_name='Описание')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    thumb = models.FileField(upload_to='images/attraction_thumb', verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Достопримечательность'
        verbose_name_plural = 'Достопримечательности'


class AttractionGallery(models.Model):
    """Галерея на странице"""
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/attraction', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Галерея'


