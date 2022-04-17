from itertools import chain

from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from hotel.models import Hotel
from region.models import Region


class HomePage(TemplateView):
    """View site page"""
    template_name = 'core/home.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['region_most_interesting_list'] = Region.objects.filter(is_most_interesting=True)
        region_popular_list = Region.objects.annotate(odd=F('id') % 2).filter(odd=False, is_popular=True)
        region_popular_list2 = Region.objects.annotate(odd=F('id') % 2).filter(odd=True, is_popular=True)
        context['region_popular_list'] = zip(region_popular_list, region_popular_list2)
        context['hotel_list_low_price'] = Hotel.objects.all()
        context['hotel_list_with_child'] = Hotel.objects.filter(child=True)
        context['hotel_list_sea'] = Hotel.objects.filter(remoteness__lte=500)
        return context


class ContactPage(TemplateView):
    """Contact page"""
    template_name = 'core/contact.html'


class AboutPage(TemplateView):
    """About company"""
    template_name = 'core/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        context['region_most_interesting_list'] = Region.objects.filter(is_most_interesting=True)
        return context

class  RentPage(TemplateView):
    """Rent room`s page"""
    template_name = 'core/rent.html'

