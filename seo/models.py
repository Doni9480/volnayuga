from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from hotel.models import TypeofObject
from region.models import Region


class SeoPage(models.Model):
    """SEO static page model"""
    title = models.CharField(max_length=50, verbose_name='Название страницы')
    slug = models.SlugField(verbose_name='URL страницы, к которой привязываем')
    h1 = models.CharField(max_length=50, blank=True, verbose_name='Заголовок H1')
    meta_title = models.TextField(blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок №1')
    content_2 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок №2')

    class Meta:
        verbose_name = 'SEO для страницы'
        verbose_name_plural = 'SEO для статических страниц'

    def __str__(self):
        return self.title


class SeoForType(models.Model):
    """SEO for type of objects"""
    city = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Город')
    type_of_object = models.ForeignKey(TypeofObject, on_delete=models.CASCADE, verbose_name='Тиж жилья')
    image_alt = models.CharField(max_length=50, blank=True, verbose_name='ALT изображения')
    image_title = models.CharField(max_length=50, blank=True, verbose_name='Title для изображения')
    meta_title = models.TextField(blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок №1')
    content_2 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок №2')

    class Meta:
        verbose_name = 'SEO для страницы типа жилья'
        verbose_name_plural = 'SEO для страниц типов жилья'

    def __str__(self):
        return f'SEO для страницы "{self.type_of_object}" в регионе {self.city}'