from django.shortcuts import render
from django.views.generic import DetailView, ListView

from hotel.models import Hotel
from .models import *





class AttractionList(ListView):
    """List of category attractions"""
    model = Attraction
    template_name = 'attraction/attraction_list.html'

    def get_queryset(self):
        return Attraction.objects.filter(category__slug=self.kwargs['category_slug'])
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context= super(AttractionList, self).get_context_data(**kwargs)
        context['attraction_category'] = AttractionCategory.objects.get(slug=self.kwargs['category_slug'])
        region = Region.objects.get(slug=self.kwargs['region_slug'])
        context['region'] = region
        context['hotel_premium_list'] = Hotel.objects.filter(city=region, premium=True)
        return context

class AttractionDetail(DetailView):
    """Attraction detail"""
    model = Attraction
    template_name = 'attraction/attraction_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AttractionDetail, self).get_context_data(**kwargs)
        context['hotel_premium_list'] = Hotel.objects.filter(premium=True, city=self.object.region)
        return context

