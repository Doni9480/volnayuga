from datetime import date

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from booking.forms import BookingCreateForm
from hotel.forms import HotelFilterForm, SearchHotelForm
from attraction.models import Attraction, AttractionCategory
from review.forms import ReviewForm
from review.models import Review
from seo.models import SeoForType, SeoForRegion, SeoForService
from .models import *
from hotel.models import Hotel, TypeofObject, HotelOption, ServiceFilterofObject
from django.views.generic import DetailView, ListView
from django.db.models import Q, F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class RegionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Region.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class RegionDetail(DetailView):
    """Обработка страницы региона"""
    model = Region

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegionDetail, self).get_context_data(**kwargs)
        try:
            context['seo'] = SeoForRegion.objects.get(city=self.object)
        except Exception:
            context['seo'] = {
                'meta_title': f'Отдых в {self.object} – недорогие цены, фото, лучшие отзывы | Вашеморе.ру',
                'meta_description': f'Отдых в {self.object} – недорогие цены, отзывы, фото номеров. Забронировать жилье без посредников: отели и гостиницы, гостевые дома, квартиры. Большое количество предложений с максимальными удобствами.',
                'h1': self.object,
                'content_1': self.object,
            }
        context['region_list'] = Region.objects.filter(parent__parent=self.object, is_city=True)
        try:
            context['region_parent_list'] = Region.objects.filter(parent=self.object.parent).exclude(
                id=self.object.id)
        except Exception:
            pass
        hotels = Hotel.objects.filter(
            Q(city__parent__parent=self.object) | Q(city__parent=self.object) | Q
            (city=self.object)).order_by('id')
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
        context['review_list'] = Review.objects.filter(verificated=True, hotel__city=self.object)
        # ids_typeofobject = Hotel.objects.filter(
        #    Q(city=self.object) | Q(city__parent=self.object) | Q(city__parent__parent=self.object)).values_list(
        #    'object_type', flat=True).distinct()
        context['type_object'] = TypeofObject.objects.all()
        context['service_object'] = ServiceFilterofObject.objects.all()
        context['filter'] = HotelFilterForm()

        paginator = Paginator(hotels, 10)

        # Из URL извлекаем номер запрошенной страницы - это значение параметра page
        page_number = self.request.GET.get('page')

        # Получаем набор записей для страницы с запрошенным номером
        page_obj = paginator.get_page(page_number)
        # Отдаем в словаре контекста
        context['hotel_list'] = page_obj
        return context


class HotelDetail(FormMixin, DetailView):
    model = Hotel
    template_name = 'hotel/hotel_detail.html'
    form_class = BookingCreateForm

    def get_success_url(self):
        return reverse_lazy('region:hotel_detail', kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(Hotel, id=pk)

    def get_context_data(self, **kwargs):
        context = super(HotelDetail, self).get_context_data(**kwargs)
        context['options_category'] = HotelOption.objects.filter(hotel=self.get_object())
        context['another_hotels'] = Hotel.objects.filter(city__slug=self.kwargs['slug']).exclude(id=self.object.id)
        context['review_form'] = ReviewForm
        context['review_list'] = Review.objects.filter(verificated=True, hotel=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.success(self.request, 'Что то пошло не так проверьте все ли заполнено!')
            return self.form_invalid(form)

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.hotel = Hotel.objects.get(id=self.kwargs['pk'])
            self.object.start_date = form.cleaned_data['start_date']
            self.object.end_date = form.cleaned_data['end_date']
            self.object.people_count = form.cleaned_data['people_count']
            self.object.save()
            messages.success(self.request, 'Вы успешно забронировали отель!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Что то пошло не так проверьте все ли заполнено!')
            return self.form_invalid(form)


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
        context['service_object'] = ServiceFilterofObject.objects.all()
        context['region_parent_list'] = Region.objects.filter(parent=self.object.parent).exclude(
            id=self.object.id)
        context['filter'] = HotelFilterForm()
        context['type_filter'] = True
        context['service_object'] = ServiceFilterofObject.objects.filter(typeofobject__slug=self.kwargs['type_slug'])
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


class HotelFilterByTypeAndService(DetailView):
    """Hotel filter by type and service block in bottom page"""
    model = Region
    template_name = 'region/filter.html'

    def get_object(self, queryset=None):
        """Возвращаем регион, чтобы остаться в нем при фильтрации"""
        return get_object_or_404(Region, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel_type = self.kwargs['type_slug']
        context['hotel_list'] = Hotel.objects.filter(
            Q(object_service__slug=self.kwargs['service_slug'], object_type__slug=self.kwargs['type_slug'],
              city=self.object) |
            Q(object_service__slug=self.kwargs['service_slug'], object_type__slug=self.kwargs['type_slug'],
              city__parent=self.object) |
            Q(object_service__slug=self.kwargs['service_slug'], object_type__slug=self.kwargs['type_slug'],
              city__parent__parent=self.object))
        context['filter'] = HotelFilterForm()
        context['type_service_filter'] = True
        context['region_parent_list'] = Region.objects.filter(parent=self.object.parent).exclude(
            id=self.object.id)
        context[
            'hotel_type'] = hotel_type  # Параметр в шаблон для определения фильтра, в зависимости от фильтра меняются ссылка критерия
        context['service_object'] = ServiceFilterofObject.objects.all()
        context['title_for_meta'] = ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])
        context['type_object'] = TypeofObject.objects.get(slug=self.kwargs['type_slug'])
        try:
            context['seo'] = SeoForService.objects.get(city=self.get_object(),
                                                       type_of_object__slug=self.kwargs['type_slug'],
                                                       service_of_object__slug=self.kwargs['service_slug'],
                                                       )
        except Exception:
            context['seo'] = {
                'meta_title': f"{ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])} {self.get_object()}",
                'meta_description': f"{ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])} {self.get_object()}",
                'h1': f"{ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])} {self.get_object()}",
                'content_1': '',
                'content_2': '',
            }
        return context


class HotelFilterByService(DetailView):
    """Hotel filter by service block in bottom page"""
    model = Region
    template_name = 'region/filter.html'

    def get_object(self, queryset=None):
        """Возвращаем регион, чтобы остаться в нем при фильтрации"""
        return get_object_or_404(Region, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_list'] = Hotel.objects.filter(
            Q(object_service__slug=self.kwargs['service_slug'], city=self.object) |
            Q(object_service__slug=self.kwargs['service_slug'],
              city__parent=self.object) |
            Q(object_service__slug=self.kwargs['service_slug'],
              city__parent__parent=self.object))
        context['filter'] = HotelFilterForm()
        context['service_object'] = ServiceFilterofObject.objects.all()
        context['service_filter'] = True
        context['region_parent_list'] = Region.objects.filter(parent=self.object.parent).exclude(
            id=self.object.id)
        context['title_for_meta'] = ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])
        try:
            context['seo'] = SeoForService.objects.get(city=self.get_object(),
                                                       type_of_object__slug=None,
                                                       service_of_object__slug=self.kwargs['service_slug']
                                                       )
        except Exception:
            context['seo'] = {
                'meta_title': f"{ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])} {self.get_object()}",
                'meta_description': f"{ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])} {self.get_object()}",
                'h1': f"{ServiceFilterofObject.objects.get(slug=self.kwargs['service_slug'])} {self.get_object()}",
                'content_1': '',
                'content_2': '',
            }
        return context


class HotelSearchBlock(ListView):
    """Search hotel date block"""
    model = Hotel
    template_name = 'region/filter.html'
    form_class = HotelFilterForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HotelSearchBlock, self).get_context_data(**kwargs)
        self.object = Region.objects.get(id=self.request.GET['city'])
        context['object'] = self.object
        context['hotel_list'] = Hotel.objects.filter(
            Q(city__parent__parent=self.object) | Q(city__parent=self.object) | Q
            (city=self.object)).order_by('id')
        context['filter'] = HotelFilterForm()
        context['service_object'] = ServiceFilterofObject.objects.all()
        context['service_filter'] = True
        context['region_parent_list'] = Region.objects.filter(parent=self.object.parent).exclude(
            id=self.object.id)
        context['form'] = SearchHotelForm
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
                hotel_list = Hotel.objects.filter(
                    Q(city__parent__parent=region, numbers__prices__price__gte=price_min,
                      numbers__prices__price__lte=price_max) | Q(city__parent=region,
                                                                 numbers__prices__price__gte=price_min,
                                                                 numbers__prices__price__lte=price_max) | Q
                    (city=region, numbers__prices__price__gte=price_min,
                     numbers__prices__price__lte=price_max)).distinct()
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

        hotel_list = hotel_list.filter(city=region, **filters)
        service_filter = True
        region_parent_list = Region.objects.filter(
            parent=region.parent).exclude(
            id=region.id)
        service_object = ServiceFilterofObject.objects.all()

    return render(request, 'region/left_filter.html', {'filter': form,
                                                       'hotel_list': hotel_list,
                                                       'object': region,
                                                       'data_filter': filters,
                                                       'region_parent_list': region_parent_list,
                                                       'service_object': service_object,
                                                       'service_filter': service_filter,
                                                       })
