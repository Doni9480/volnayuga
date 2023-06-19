from itertools import chain
from typing import Any
from django import http

from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView, FormView

from hotel.forms import SearchHotelForm
from review.models import Review
from seo.models import SeoPage
from hotel.models import Hotel
from region.models import Region
from userQueries.forms import FeedbackForm
from django.core.mail import send_mail, BadHeaderError
import os


class HomePage(TemplateView):
    """Home page"""
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
        context['review_list'] = Review.objects.filter(verificated=True)
        context['form'] = SearchHotelForm
        try:
            context['object'] = SeoPage.objects.get(slug='home')
        except Exception:
            context['object'] = {
                'meta_title': 'meta_title',
                'meta_description': 'meta_description',
                'h1': 'h1',
                'content_1': 'Создай страницу в админке',
                'content_2': 'Создай страницу в админке',
            }
        return context


class ContactPage(FormView):
    """Contact page"""
    template_name = 'core/contact.html'
    form_class = FeedbackForm
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['object'] = SeoPage.objects.get(slug='contact')
        except Exception:
            context['object'] = {
                'meta_title': 'meta_title',
                'meta_description': 'meta_description',
                'h1': 'h1',
                'content_1': 'Создай страницу в админке',
                'content_2': 'Создай страницу в админке',
                'phone_1': 'Можно добавить в админке',
                'phone_2': 'Можно добавить в админке',
                'email_1': 'Можно добавить в админке',
                'email_2': 'Можно добавить в админке',
                'address': 'Можно добавить в админке',
                'requisite_1': 'Можно добавить в админке',
                'requisite_2': 'Можно добавить в админке',
            }
        return context

    def form_valid(self, form):
        try:
            send_mail(subject=f"Запрос на обратную связ - {form.cleaned_data['name']}",
            message=f"Имя: {form.cleaned_data['name']}\nНомер телефона: {form.cleaned_data['phone']}\n\n{form.cleaned_data['message']}",
            from_email=f'{os.environ.get("EMAIL_HOST_USER")}',
            recipient_list=[f"{os.environ.get('ADMIN_EMAIL')}"],
            fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        form.save()
        return super().form_valid(form)


class AboutPage(TemplateView):
    """About company"""
    template_name = 'core/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        try:
            context['object'] = SeoPage.objects.get(slug='about')
        except Exception:
            context['object'] = {
                'meta_title': 'meta_title',
                'meta_description': 'meta_description',
                'h1': 'h1',
                'content_1': 'Создай страницу в админке',
                'content_2': 'Создай страницу в админке',
            }
        context['region_most_interesting_list'] = Region.objects.filter(is_most_interesting=True)
        return context


class RentPage(TemplateView):
    """Rent room`s page"""
    template_name = 'core/rent.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RentPage, self).get_context_data(**kwargs)
        try:
            context['object'] = SeoPage.objects.get(slug='rent')
        except Exception:
            context['object'] = {
                'meta_title': 'meta_title',
                'meta_description': 'meta_description',
                'h1': 'h1',
                'content_1': 'Создай страницу в админке',
                'content_2': 'Создай страницу в админке',
            }
        return context
