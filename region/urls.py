from django.urls import path, include
from django_filters.views import FilterView

from hotel.models import Hotel
from region.models import Region
from region.views import HotelDetail, HotelFilterByType, hotel_list, HotelFilterLeftBlock, HotelFilterByService
from region.views import RegionDetail

app_name = 'region'

urlpatterns = [
    path('', RegionDetail.as_view(), name='region_detail'),
    path('filter/', hotel_list, name='hotel_filter_left'),
    path('<int:pk>/', HotelDetail.as_view(), name='hotel_detail'),
    path('<slug:type_slug>/', HotelFilterByType.as_view(), name='hotel_type_filter'),
    path('s/<slug:service_slug>/', HotelFilterByService.as_view(), name='hotel_service_filter'),
    path('<slug:type_slug>/<slug:service_slug>/', HotelFilterByService.as_view(), name='hotel_service_filter'),

]
