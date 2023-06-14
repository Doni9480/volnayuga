from django.urls import path
from .views import CreateBooking

app_name = 'booking'

urlpatterns = [
    path('create/<hotel_id>/', CreateBooking.as_view(), name='create-booking'),
]
