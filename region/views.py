from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import *
from hotel.models import Hotel
from django.views.generic import DetailView, ListView
from django.db.models import Q



# Create your views here.


class RegionList(DetailView):
    """Обработка страницы региона"""
    model = Region
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegionList, self).get_context_data(**kwargs)
        context['region_popular_list'] = Region.objects.filter(Q(parent__parent=self.object, is_city=True,
                                                               is_popular=True) | Q(parent=self.object, is_city=True,
                                                               is_popular=True))
        context['region_list'] = Region.objects.filter(parent__parent=self.object, is_city=True)
        context['region_parent_list'] = Region.objects.filter(parent=self.object)
        context['hotel_list'] = Hotel.objects.filter(Q(city__parent__parent=self.object) | Q(city__parent=self.object) |Q
                                                     (city=self.object))
        return context




class HotelDetail(DetailView):
    model = Hotel

    def get_object(self, queryset=None):
        return Hotel.objects.get(city__slug=self.kwargs['slug'],slug=self.kwargs['hotel_slug'])

