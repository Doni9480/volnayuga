from datetime import date

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from hotel.forms import HotelFilterForm, HotelFilter
from attraction.models import Attraction, AttractionCategory
from review.models import Review
from seo.models import SeoForType, SeoForRegion
from .models import *
from hotel.models import Hotel, Number, TypeofObject, HotelOption, PricePeriod
from django.views.generic import DetailView, ListView
from django.db.models import Q, F


class RegionDetail(DetailView):
    """Обработка страницы региона"""
    model = Region

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegionDetail, self).get_context_data(**kwargs)
        try:
            context['seo'] = SeoForRegion.objects.get(city=self.object)
        except Exception:
            context['seo'] = {
                'meta_title': self.object,
                'meta_description': self.object,
                'h1': self.object,
                'content_1': self.object,
            }
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
        #ids_typeofobject = Hotel.objects.filter(
        #    Q(city=self.object) | Q(city__parent=self.object) | Q(city__parent__parent=self.object)).values_list(
        #    'object_type', flat=True).distinct()
        context['typeobject'] = TypeofObject.objects.all()
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
    template_name = 'region/filter.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Region, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(HotelFilterByType, self).get_context_data(**kwargs)
        context['hotel_list'] = Hotel.objects.filter(Q(object_type__slug=self.kwargs['type_slug'], city=self.object) |
                                                     Q(object_type__slug=self.kwargs['type_slug'],
                                                       city__parent=self.object) |
                                                     Q(object_type__slug=self.kwargs['type_slug'],
                                                       city__parent__parent=self.object))
        context['filter'] = HotelFilterForm()
        context['title_for_meta'] = TypeofObject.objects.get(slug=self.kwargs['type_slug'])
        try:
            context['seo'] = SeoForType.objects.get(city=self.get_object(),
                                                    type_of_object__slug=self.kwargs['type_slug'])
        except Exception:
            context['seo'] = {
                'meta_title': f"{TypeofObject.objects.get(slug=self.kwargs['type_slug'])} {self.get_object()}",
                'meta_description': f"{TypeofObject.objects.get(slug=self.kwargs['type_slug'])} {self.get_object()}",
                'h1': f"{TypeofObject.objects.get(slug=self.kwargs['type_slug'])} {self.get_object()}",
                'content_1': '',
                'content_2': '',
            }
        return context

        return context


class HotelFilterLeftBlock(ListView):
    """Ajax filter in left block"""
    model = Hotel
    template_name = 'region/filter.html'
    form_class = HotelFilterForm

    def get_queryset(self):
        data = 'ss'
        return data


def hotel_list(request, slug):
    form = HotelFilterForm(request.GET)
    region = Region.objects.get(slug=slug)
    if request.GET:
        request.GET._mutable = True
        request.GET.pop('submit', None)
        filters = {}
        options_ids = []
        remoteness_ids = []
        beach_ids = []
        for param, value in request.GET.items():
            if param == 'range_1' or param == 'range_2':
                price_min = int(request.GET.get('range_1')) * 100
                price_max = int(request.GET.get('range_2')) * 100
                hotel_list = Hotel.objects.filter(city=region, number__price__price__gte=price_min,
                                                  number__price__price__lte=price_max).distinct()
            elif param == 'object_type':
                list_id = []
                for i in request.GET.getlist('object_type'):
                    list_id.append(i)
                filters['{}__in'.format(param)] = list_id
            elif param == 'options_food':
                param = 'options'
                for i in request.GET.getlist('options_food'):
                    options_ids.append(i)
                filters['{}__in'.format(param)] = options_ids
            elif param == 'options_service':
                param = 'options'
                for i in request.GET.getlist('options_service'):
                    options_ids.append(i)
                filters['{}__in'.format(param)] = options_ids
            elif param == 'options_booking':
                param = 'options'
                for i in request.GET.getlist('options_booking'):
                    options_ids.append(i)
                filters['{}__in'.format(param)] = options_ids
            elif param == 'beach':
                for i in request.GET.getlist('beach'):
                    beach_ids.append(i)
                filters['{}__in'.format(param)] = beach_ids
            elif param == 'remoteness':
                for i in request.GET.getlist('remoteness'):
                    remoteness_ids.append(i)
                filters['{}__in'.format(param)] = remoteness_ids

            # # elif param == 'beach':
            # #     filters['{}'.format(param)] = value
            # # elif param == 'object_type':
            # #     filters['{}'.format(param)] = value
            #
            # else:
        hotel_list = hotel_list.filter(city=region, **filters)

        # option_list = []
        # options = request.GET
        # if 'options_service' or 'options_food' or 'options_booking' in options:
        #     options_service = request.GET.getlist('options_service')
        #     for item in options_service:
        #         option_list.append(item)
        #     options_food = request.GET.getlist('options_food')
        #     for item in options_food:
        #         option_list.append(item)
        #     options_booking = request.GET.getlist('options_booking')
        #     for item in options_booking:
        #         option_list.append(item)
        #
        #     hotel_list = Hotel.objects.filter(options__in=option_list).distinct()
        #
        # if 'range_1' and 'range_2' in options:
        #     price_min = int(request.GET.get('range_1')) * 100
        #     price_max = int(request.GET.get('range_2')) * 100
        #
        #     hotel_list = Hotel.objects.filter(number__price__price__gte=price_min, number__price__price__lte=price_max).distinct()
        #
        #

    return render(request, 'region/filter.html', {'filter': form,
                                                  'hotel_list': hotel_list,
                                                  'object': region,
                                                  'data_filter': filters,
                                                  })
