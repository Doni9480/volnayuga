from datetime import datetime
from django.db import models

from hotel.models import Hotel


class Review(models.Model):
    """Отзыв с оценкой"""
    name = models.CharField(max_length=300, verbose_name='Имя')
    city = models.CharField(max_length=200, blank=True, verbose_name='Город')
    born = models.DateField(default=datetime.now, verbose_name='Дата создания')
    period = models.CharField(max_length=50, verbose_name='Период отдыха')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default='5', verbose_name='Рейтинг')
    body = models.TextField(verbose_name='Описание')
    email = models.EmailField()
    verificated = models.BooleanField(default=False, verbose_name='Активен')

    class Meta:
        verbose_name_plural = '    Отзывы'
        verbose_name = 'Отзыв'

    def __str__(self):
        return "%s: %s" % (self.name, self.hotel)
