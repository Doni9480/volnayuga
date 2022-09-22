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



