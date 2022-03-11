from django.db import models
from accounts.models import MyUser
from ckeditor.fields import RichTextField
from region.models import Region



class Type_of_Object(models.Model):
    """Типы объектов сдачи"""
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = ' Типы объектов размещения'

    def __str__(self):
        return self.title



class Beach(models.Model):
    """Выбор типа пляжа"""
    title = models.CharField(max_length=100, verbose_name='Название')
    class Meta:
        verbose_name = 'Пляж'
        verbose_name_plural = 'Пляжи'

    def __str__(self):
        return self.title


class Number_option(models.Model):
    """Опции объекта"""
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Опцию'
        verbose_name_plural = ' Опции для номеров'

    def __str__(self):
        return self.title

class Hotel_option(models.Model):
    """Опции объекта"""
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Опцию'
        verbose_name_plural = ' Опции для гостиниц'

    def __str__(self):
        return self.title
    
class Hotel_contact(models.Model):
    """Контакты объекта"""
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    photo = models.FileField(upload_to='images/contacts', verbose_name='Фотография')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    skype = models.BooleanField(default=0)
    whatsapp = models.BooleanField(default=0)
    telegram = models.BooleanField(default=0)
    viber = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты объектов размещения'

    def __str__(self):
        return self.phone


class Hotel(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL', default='1')
    object_type = models.ForeignKey(Type_of_Object, on_delete=models.CASCADE, verbose_name='Тип объекта')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    city = models.ForeignKey(Region, on_delete=models.CASCADE, limit_choices_to={'is_city': True},verbose_name='Город')
    remoteness = models.IntegerField(null=True, blank=True,verbose_name='Удаленность от пляжа')
    beach = models.ForeignKey(Beach, on_delete=models.CASCADE, verbose_name='Пляж')
    options = models.ManyToManyField(Hotel_option, verbose_name='Опции')
    contact = models.ForeignKey(Hotel_contact, on_delete=models.CASCADE, verbose_name='Контакты')
    description = RichTextField(blank=True, verbose_name='Описание')
    video = models.URLField(blank=True, verbose_name='Видео объекта')
    number = models
    prepayment = models.CharField(max_length=10, blank=True,verbose_name='Предоплата')
    free_cancel = models.CharField(max_length=100, blank=True, verbose_name='Условия бесплатной отмены брони')
    early_booking_discount = models.IntegerField(null=True, blank=True, verbose_name='Скидка на раннее бронирование')
    requisites = models.TextField(blank=True, verbose_name='Реквизиты')
    prepayments_term = models.BooleanField(default=0, verbose_name='Без предоплаты')
    minimum = models.IntegerField(blank=True, verbose_name='Минимальный срок проживания в сутках')
    chek_in = models.TimeField(blank=True, verbose_name='Время заселения')
    chek_out = models.TimeField(blank=True, verbose_name='Время выезда')
    pets = models.BooleanField(default=0, verbose_name='Животные')
    child = models.BooleanField(default=0, verbose_name='Дети')
    another_rules = models.TextField(blank=True, verbose_name='Другие правила')

    class Meta:
        verbose_name = ' Обьект размещения'
        verbose_name_plural = ' Гостиницы'

    def __str__(self):
        return self.title


class Photo_in_filter(models.Model):
    """Фотографии на странице фильтрации"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/hotel_photo_thumb', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии объекта для страниц фильтрации'

class Photo_on_detail(models.Model):
    """Фотографии на детальной странице"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/hotel_photo', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии объекта для страницы объекта'


class Number(models.Model):
    hotel = models.ForeignKey(Hotel, default=1, on_delete=models.CASCADE, verbose_name='Отель')
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    room_number = models.IntegerField(null=True, blank=True, verbose_name='Количество комнат')
    sleep_place = models.IntegerField(null=True, blank=True, verbose_name='Количество спальных мест')
    room_square = models.IntegerField(null=True, blank=True, verbose_name='Площадь комнаты')
    additional_palces = models.IntegerField(null=True, blank=True, verbose_name='Дополнительные места')
    furniture =  models.TextField(blank=True, verbose_name='Мебель')
    options = models.ManyToManyField(Number_option, verbose_name='Опции')

    class Meta:
        verbose_name = ' Номер'
        verbose_name_plural = ' Номера'

    def __str__(self):
        return self.title

class Number_photo(models.Model):
    """Фотографии номера"""
    number = models.ForeignKey(Number, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/numbers', verbose_name='Изображение')


