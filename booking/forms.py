from django import forms

from booking.models import HotelBooking


class BookingCreate(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = '__all__'
        exclude = ('hotel',)
