from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
# Create your models here.
from django.db.models import Min, Avg, Q



class Region(models.Model):
    """Направления"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    short_description = models.TextField(blank=True, verbose_name='Короткое описание в шапке')
    is_city = models.BooleanField(default=False, verbose_name='Если город, то ставь галочку!')
    is_popular = models.BooleanField(default=False, verbose_name='Показывать в блоке популярные на главной')
    is_most_interesting = models.BooleanField(default=False, verbose_name='Показывать на главной в первом блоке')
    image = models.FileField(upload_to='region', verbose_name='Изображение')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родитель',
                               related_name='children')
    season = models.CharField(max_length=100, null=True, blank=True,
                              verbose_name='Задайте сезон, например(январь-февраль)')

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = ' Направления'

    def __str__(self):
        return self.title

    def get_min_price(self):
        return self.hotel_set.all().aggregate(min_price=Min('periods__price__price'))['min_price']

    def get_average_price(self):
        from hotel.models import Hotel
        if self.is_most_interesting:
            hotel_list = Hotel.objects.filter(
                Q(city__parent__parent__parent=self) | Q(city__parent=self) | Q(city=self) | Q(
                    city__parent__parent=self))
            return hotel_list.aggregate(average=Avg('periods__prices__price'))['average']

        elif self.is_city:
            hotel_list = Hotel.objects.filter(city=self)
            return hotel_list.aggregate(average=Avg('periods__prices__price'))['average']

        elif self.parent:
            hotel_list = Hotel.objects.filter(city__parent=self)
            return hotel_list.aggregate(average=Avg('priceperiod__prices__price'))['average']
        else:
            hotel_list = Hotel.objects.filter(city__parent__parent__parent=self)
            return hotel_list.aggregate(average=Avg('priceperiod__price__price'))['average']

    def get_average_review(self):
        from hotel.models import Hotel

        if self.is_most_interesting:
            hotel_list = Hotel.objects.filter(
                Q(city__parent__parent__parent=self) | Q(city__parent=self) | Q(city=self) | Q(
                    city__parent__parent=self))
            return hotel_list.aggregate(average=Avg('review__rating'))['average']

        elif self.is_city:
            hotel_list = Hotel.objects.filter(city=self)
            return hotel_list.aggregate(average=Avg('review__rating'))['average']

        elif self.parent:
            hotel_list = Hotel.objects.filter(city__parent=self)
            return hotel_list.aggregate(average=Avg('review__rating'))['average']
        else:
            hotel_list = Hotel.objects.filter(city__parent__parent__parent=self)
            return hotel_list.aggregate(average=Avg('review__rating'))['average']


class GalleryForRegion(models.Model):
    """Фотографии для региона"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    image = models.ImageField(upload_to='images/region', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Галерея для региона'
