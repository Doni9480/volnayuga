from datetime import date

from django.db import models
from django.db.models import Avg, Sum, Min

from accounts.models import MyUser
from ckeditor.fields import RichTextField

from region.models import Region


class TypeofObject(models.Model):
    """Типы объектов сдачи"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='hotel/hoteltype', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = ' Типы объектов размещения'

    def __str__(self):
        return self.title

class ServiceFilterofObject(models.Model):
    """Фильтр критериев удобств объектов сдачи"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='hotel/filterservice', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Критерий удобства'
        verbose_name_plural = ' Критерии удобства'

    def __str__(self):
        return self.title


OPTIONCATEGORYCHOICE = (
    ('food', ('Питание')),
    ('service', ('Удобства и услуги')),
    ('booking', ('Условия бронирования')),
)


class HotelOption(models.Model):
    """Опции объекта"""
    title = models.CharField(max_length=100, verbose_name='Название')
    comment = models.CharField(max_length=100, blank=True, verbose_name='Комментарии')
    category = models.CharField(max_length=50, choices=OPTIONCATEGORYCHOICE, default='food', verbose_name='Категория')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Класс иконки font-awesome')

    class Meta:
        verbose_name = 'Опцию'
        verbose_name_plural = ' Опции для гостиниц'

    def __str__(self):
        return self.title


class Distance(models.Model):
    """Расстояния от гостиницы"""
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Расстояние до обьекта'
        verbose_name_plural = 'Расстояния до объектов'

    def __str__(self):
        return self.title


WALKMETHODCHOICE = (
    ('walk', ('Пешком')),
    ('avto', ('На авто')),
)


class DistanceTime(models.Model):
    """Расстояние до объектов"""
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE, verbose_name='Объект расстояния')
    time = models.IntegerField(verbose_name='Время', blank=True, null=True)
    method = models.CharField(max_length=10, choices=WALKMETHODCHOICE, blank=True, null=True, verbose_name='Метод')
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Гостиница')

    class Meta:
        verbose_name = 'Время до обьекта'
        verbose_name_plural = 'Время до объектов'


BEACHCHOICE = (
    ('galka', ('Галька')),
    ('pesok', ('Песок')),
)

BEACHREMOTENESS = [
    ('100', '100'),
    ('200', '200'),
    ('500', '500'),
    ('800', '800'),
    ('1000', '1000'),
    ('1500', '1500'),
]

class Hotel(models.Model):
    """Отель"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.CharField(max_length=100, verbose_name='Название')
    meta_title = models.CharField(max_length=100, blank=True, verbose_name='Мета заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Мета описание')
    premium = models.BooleanField(default=False, verbose_name='Премиум гостиница')
    object_type = models.ManyToManyField(TypeofObject, blank=True, verbose_name='Тип жилья')
    object_service = models.ManyToManyField(ServiceFilterofObject, blank=True, verbose_name='Фильтр по критериям жилья')
    address = models.CharField(max_length=100, verbose_name='Адрес (без указания города)')
    city = models.ForeignKey(Region, on_delete=models.CASCADE, limit_choices_to={'is_city': True}, verbose_name='Город')
    remoteness = models.CharField(max_length=10, blank=True, choices=BEACHREMOTENESS, default=1, verbose_name='Расстояние до моря')
    beach = models.CharField(max_length=50, blank=True, choices=BEACHCHOICE, default='1000', verbose_name='Пляж')
    centr = models.CharField(max_length=20, blank=True, verbose_name='Расстояние до центра')
    options = models.ManyToManyField(HotelOption, blank=True, verbose_name='Опции')
    description = RichTextField(blank=True, verbose_name='Описание')
    video = models.URLField(blank=True, verbose_name='Ссылка на видео объекта')
    distance = models.ManyToManyField(Distance, through='DistanceTime')
    prepayment = models.CharField(max_length=10, blank=True,
                                  verbose_name='Размер предоплаты в % или в сутках проживания')
    free_cancel = models.CharField(max_length=100, blank=True, verbose_name='Условия бесплатной отмены брони')
    early_booking_discount = models.IntegerField(null=True, blank=True, verbose_name='Скидка на раннее бронирование')
    requisites = models.TextField(blank=True, verbose_name='Реквизиты')
    prepayments_term = models.BooleanField(default=0, verbose_name='Без предоплаты')
    minimum = models.IntegerField(blank=True, null=True, verbose_name='Минимальный срок проживания в сутках')
    chek_in = models.TimeField(blank=True, null=True, verbose_name='Время заселения')
    chek_out = models.TimeField(blank=True, null=True, verbose_name='Время выезда')
    pets = models.BooleanField(default=0, verbose_name='Размещение животных')
    child = models.BooleanField(default=0, verbose_name='Размещение детей')
    another_rules = models.TextField(blank=True, verbose_name='Другие правила')

    class Meta:
        verbose_name = ' Обьект размещения'
        verbose_name_plural = ' Гостиницы'

    def __str__(self):
        return self.title

    def get_min_price(self):
        return self.number_set.all().aggregate(min_price=Min('price__price'))['min_price']


class HotelPhoto(models.Model):
    """Фотографии на странице фильтрации"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='hotel/hotel_photo_thumb', null=True, default='profile_image/none/no-img.png',
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии объекта для страниц фильтрации'

    def __str__(self):
        return self.image.name


class HotelContact(models.Model):
    """Контакты объекта"""
    hotel = models.ForeignKey(Hotel, default=1, on_delete=models.CASCADE, verbose_name='Гостиница')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    photo = models.FileField(upload_to='hotel/contacts', null=True, blank=True, verbose_name='Фотография')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    skype = models.BooleanField(default=0)
    whatsapp = models.BooleanField(default=0)
    telegram = models.BooleanField(default=0)
    viber = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты объектов размещения'

    def __str__(self):
        return self.name


class NumberOption(models.Model):
    """Опции объекта"""
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Опцию'
        verbose_name_plural = ' Опции для номеров'

    def __str__(self):
        return self.title


class Number(models.Model):
    ORDERCHOICE = (
        ('number', ('за номер')),
        ('people', ('за человека')),
    )

    order_choice = models.CharField(max_length=10, choices=ORDERCHOICE, default='за номер',
                                    verbose_name='Цена в объявлении')
    hotel = models.ForeignKey(Hotel, default=1, on_delete=models.CASCADE, verbose_name='Отель')
    title = models.CharField(max_length=100, verbose_name='Название')
    room_number = models.IntegerField(null=True, blank=True, verbose_name='Количество комнат')
    sleep_place = models.IntegerField(null=True, blank=True, verbose_name='Количество спальных мест')
    room_square = models.IntegerField(null=True, blank=True, verbose_name='Площадь комнаты')
    additional_palces = models.IntegerField(null=True, blank=True, verbose_name='Дополнительные места')
    furniture = RichTextField(blank=True, verbose_name='Мебель')
    options = models.ManyToManyField(NumberOption, blank=True, verbose_name='Опции')

    class Meta:
        verbose_name = ' Номер'
        verbose_name_plural = ' Номера'

    def __str__(self):
        return self.hotel.title + ' - ' + self.title

    def get_min_price(self):
        """Самая низкая цена номера"""
        return Price.objects.filter(number=self).aggregate(min_price=Min('price'))['min_price']

    def get_price_today(self):
        """Цена номера на сегодня"""
        today = date.today()
        number_price_list = Price.objects.filter(number=self)
        for item in number_price_list:
            if today >= item.period.start and today <= item.period.end:
                return item.price
            else:
                return self.get_min_price()


class PricePeriodToday(models.Manager):
    """Today manager"""

    def get_queryset(self):
        return super(PricePeriodToday, self).get_queryset().filter(start__lte=date.today(), end__gte=date.today())


class PricePeriod(models.Model):
    """Периоды цен"""
    start = models.DateField(verbose_name='Начало периода')
    end = models.DateField(verbose_name='Конец периода')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Гостиница')
    objects = models.Manager()
    today = PricePeriodToday()

    class Meta:
        verbose_name = 'Календарные периоды цен'
        verbose_name_plural = 'Период цен'
        ordering = ['start']

    def __str__(self):
        return f'{self.hotel} период цен с {self.start} по {self.end}'


class Price(models.Model):
    """Number Price"""

    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    extra_bed = models.IntegerField(null=True, blank=True, verbose_name='Цена за дополнительное место')
    number = models.ForeignKey(Number, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Номер')
    period = models.ForeignKey(PricePeriod, on_delete=models.CASCADE, verbose_name='Период')

    class Meta:
        verbose_name = 'Цены'
        verbose_name_plural = 'Цены гостиницы'
        ordering = ['period__start']

    def __str__(self):
        return f'Цены'


class NumberPhoto(models.Model):
    """Фотографии номера"""
    number = models.ForeignKey(Number, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel/numbers', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографии номера'
        verbose_name_plural = 'Фотографии номера'
