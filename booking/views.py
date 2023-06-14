from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from booking.forms import BookingCreate
from booking.models import HotelBooking
from hotel.models import Hotel


class CreateBooking(CreateView):
    """Создание объекта бронирования"""
    model = HotelBooking
    form_class = BookingCreate

    def get_success_url(self):
        return reverse('region:hotel_detail', args={'slug:tuapse', 'pk:1'})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.hotel = Hotel.objects.get(id=self.kwargs['hotel_id'])
        self.object.start_date = form.cleaned_data['start_date']
        self.object.start_date = form.cleaned_data['end_date']
        self.object.people_count = form.cleaned_data['people_count']
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
