from django.shortcuts import render
from .models import *
from core.models import Hotel
from django.views.generic import DetailView, ListView


# Create your views here.


class RegionList(DetailView):
    model = Region


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegionList, self).get_context_data(**kwargs)
        context['hotel_list'] = Hotel.objects.filter(city=self)
        return context

