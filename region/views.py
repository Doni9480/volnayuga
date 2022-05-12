from datetime import date

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from accounts.forms import HotelFilterForm
from attraction.models import Attraction, AttractionCategory
from hotel.filter import ProductFilter
from review.models import Review
from .models import *
from hotel.models import Hotel, Number, TypeofObject, HotelOption, PricePeriod
from django.views.generic import DetailView, ListView
from django.db.models import Q, F


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
            Q(odd=False, parent__parent=self.object, is_popular=True) | Q(odd=False, parent=self.object,
                                                                          is_popular=True))
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
        ids_typeofobject = Hotel.objects.filter(
            Q(city=self.object) | Q(city__parent=self.object) | Q(city__parent__parent=self.object)).values_list(
            'object_type', flat=True).distinct()
        context['typeobject'] = TypeofObject.objects.filter(id__in=ids_typeofobject)
        context['filter'] = HotelFilterForm()
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


class HotelFilterByType(DetailView):
    """Filter by object`s type"""
    model = Region
    template_name = 'region/hotel_filter.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Region, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(HotelFilterByType, self).get_context_data(**kwargs)
        region = Region.objects.get(slug=self.kwargs['slug'])
        context['hotel_list'] = region.hotel_set.filter(object_type__slug=self.kwargs['type_slug'])
        context['filter'] = HotelFilterForm()
        context['title_for_meta'] = TypeofObject.objects.get(slug=self.kwargs['type_slug'])
        return context
