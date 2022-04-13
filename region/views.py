from datetime import date

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from attraction.models import Attraction, AttractionCategory
from review.models import Review
from .models import *
from hotel.models import Hotel, Number, TypeofObject, HotelOption, PricePeriod
from django.views.generic import DetailView, ListView
from django.db.models import Q, F


class Home(ListView):
    """Home page"""
    model = Region
    template_name = 'region/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['region_most_interesting_list'] = Region.objects.filter(is_most_interesting=True)
        region_popular_list = Region.objects.annotate(odd=F('id') % 2).filter(odd=False, is_popular=True)
        region_popular_list2 = Region.objects.annotate(odd=F('id') % 2).filter(odd=True, is_popular=True)
        context['region_popular_list'] = region_popular_list, region_popular_list2
        context['hotel_list_low_price'] = Hotel.objects.all()
        context['hotel_list_with_child'] = Hotel.objects.filter(child=True)
        context['hotel_list_sea'] = Hotel.objects.filter(remoteness__lte=500)

        return context


class RegionDetail(DetailView):
    """Обработка страницы региона"""
    model = Region

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegionDetail, self).get_context_data(**kwargs)
        context['region_list'] = Region.objects.filter(parent__parent=self.object, is_city=True)
        context['region_parent_list'] = Region.objects.filter(parent=self.object)
        context['hotel_list'] = Hotel.objects.filter(
            Q(city__parent__parent=self.object) | Q(city__parent=self.object) | Q
            (city=self.object))
        context['hotel_type'] = TypeofObject.objects.all()  # Подборка жилья по типу
        region_popular_list = Region.objects.annotate(odd=F('id') % 2).filter(
            Q(odd=False, parent__parent=self.object, is_popular=True) | Q(odd=False, parent=self.object,is_popular=True))
        region_popular_list2 = Region.objects.annotate(odd=F('id') % 2).filter(
            Q(odd=True, parent__parent=self.object, is_popular=True) | Q(odd=True, parent=self.object, is_popular=True))
        context['region_popular_list'] = zip(region_popular_list, region_popular_list2)
        context['region_attraction_list'] = Attraction.objects.filter(
            Q(region__parent__parent=self.object) | Q(region=self.object
                                                      ) | Q(region__parent=self.object))
        context['attraction_category_list'] = AttractionCategory.objects.all()

        context['hotel_premium_list'] = Hotel.objects.filter(
            Q(city__parent=self.object, premium=True) | Q(city__parent__parent=self.object, premium=True))
        context['today'] = date.today()
        context['review_list'] = Review.objects.filter(hotel__city=self.object)
        return context


class HotelDetail(DetailView):
    model = Hotel
    template_name = 'hotel/hotel_detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(Hotel, id=pk)

    def get_context_data(self, **kwargs):
        context = super(HotelDetail, self).get_context_data(**kwargs)
        context['options_category'] = HotelOption.objects.filter(hotel=self.get_object())
        context['another_hotels'] = Hotel.objects.filter(city__slug=self.kwargs['slug']).exclude(id=self.object.id)
        return context
