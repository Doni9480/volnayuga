import datetime

from django.db import models
from django.utils.timezone import now
from hotel.models import Hotel


class HotelBooking(models.Model):
    """Модель бронирования"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Объект')
    start_date = models.DateField(default=now, verbose_name='Дата начала')
    end_date = models.DateField(default=now, verbose_name='Дата окончания')
    people_count = models.IntegerField(default=2, verbose_name='Количество гостей')

    class Meta:
        verbose_name = 'Бронирования'
        verbose_name_plural = 'Бронирование'

    def __str__(self):
        return f'{self.hotel} | {self.start_date} - {self.end_date}'
