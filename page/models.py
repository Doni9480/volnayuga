from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Страница')
    url = models.SlugField(unique=True)
    content = RichTextUploadingField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title


class StatusCode(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название страницы')
    h1 = models.CharField(max_length=50, blank=True, verbose_name='Заголовок H1')
    header_text = RichTextUploadingField(blank=True, verbose_name='Текст под заголовком')
    content_1 = RichTextUploadingField(blank=True, verbose_name='Текстовый блок')

    class Meta:
        verbose_name = 'Обработчик исключений'
        verbose_name_plural = 'Обработчики исключений'

    def __str__(self):
        return self.title
