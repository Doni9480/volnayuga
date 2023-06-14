from django import forms

from booking.models import HotelBooking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = '__all__'
        exclude = ('hotel',)
