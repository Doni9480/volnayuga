from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from hotel.models import TypeofObject, ServiceFilterofObject
from page.models import Page
from region.models import Region


class SeoPage(models.Model):
    """SEO static page model."""
    title = models.CharField(max_length=50, verbose_name='Название страницы')
    slug = models.CharField(max_length=50, verbose_name='URL страницы, к которой привязываем')
    h1 = models.CharField(max_length=50, blank=True, verbose_name='Заголовок H1')
    header_text = models.TextField(blank=True, verbose_name='Текст под заголовком')
    meta_title = models.TextField(blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок №1')
    content_2 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок №2')
    phone_1 = models.CharField(max_length=15,blank=True, verbose_name='Телефон 1 (Страница контакты)')
    phone_2 = models.CharField(max_length=15,blank=True, verbose_name='Телефон 2 (Страница контакты)')
    email_1 = models.EmailField(blank=True, verbose_name='Электронная почта 1 (Страница контакты)')
    email_2 = models.EmailField(blank=True, verbose_name='Электронная почта 2 (Страница контакты)')
    address = models.TextField(blank=True, verbose_name='Адрес (Страница контакты)')
    requisite_1 = models.CharField(max_length=100,blank=True, verbose_name='Реквизит 1 (Страница контакты)')
    requisite_2 = models.CharField(max_length=100,blank=True, verbose_name='Реквизит 2 (Страница контакты)')

    class Meta:
        verbose_name = 'SEO для страницы'
        verbose_name_plural = 'SEO для статических страниц'

    def __str__(self):
        return self.title


class SeoForType(models.Model):
    """SEO for type of objects."""
    city = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Город')
    type_of_object = models.ForeignKey(TypeofObject, on_delete=models.CASCADE, verbose_name='Тиж жилья')
    image_alt = models.CharField(max_length=50, blank=True, verbose_name='ALT изображения')
    image_title = models.CharField(max_length=50, blank=True, verbose_name='Title для изображения')
    meta_title = models.TextField(blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    h1 = models.CharField(max_length=50, blank=True, verbose_name='H1 заголовок')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок')

    class Meta:
        verbose_name = 'SEO для страницы типа жилья'
        verbose_name_plural = 'SEO для страниц типов жилья'

    def __str__(self):
        return f'SEO для страницы "{self.type_of_object}" в регионе {self.city}'


class SeoForService(models.Model):
    """SEO for service of objects."""
    city = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Город')
    service_of_object = models.ForeignKey(ServiceFilterofObject, on_delete=models.CASCADE, verbose_name='Критерий жилья')
    type_of_object = models.ForeignKey(TypeofObject, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Тиж жилья')
    image_alt = models.CharField(max_length=50, blank=True, verbose_name='ALT изображения')
    image_title = models.CharField(max_length=50, blank=True, verbose_name='Title для изображения')
    meta_title = models.TextField(blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    h1 = models.CharField(max_length=50, blank=True, verbose_name='H1 заголовок')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок')

    class Meta:
        verbose_name = 'SEO для страницы критерия жилья'
        verbose_name_plural = 'SEO для страниц критериев жилья'

    def __str__(self):
        return f'SEO для страницы фильтра "{self.city} -> {self.type_of_object} -> {self.service_of_object}"'


class SeoForRegion(models.Model):
    """SEO for region page."""
    city = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Город')
    image_alt = models.CharField(max_length=50, blank=True, verbose_name='ALT изображения')
    image_title = models.CharField(max_length=50, blank=True, verbose_name='Title для изображения')
    meta_title = models.TextField(blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    h1 = models.CharField(max_length=50, blank=True, verbose_name='H1 заголовок')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок')

    class Meta:
        verbose_name = 'SEO для региона'
        verbose_name_plural = 'SEO для регионов'

    def __str__(self):
        return f'SEO для региона "{self.city}"'
    
