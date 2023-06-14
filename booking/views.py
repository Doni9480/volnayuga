from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from booking.forms import BookingCreateForm
from booking.models import HotelBooking
from hotel.models import Hotel


class CreateBooking(CreateView):
    """Создание объекта бронирования"""
    model = HotelBooking
    form_class = BookingCreateForm

    def get_success_url(self):
        return reverse('region:hotel_detail', args={'slug:tuapse', 'pk:1'})


