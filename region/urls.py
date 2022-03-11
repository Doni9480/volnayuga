from django.urls import path, include
from region.views import HotelDetail
from region.views import RegionList



urlpatterns = [
    path('<hotel_slug>', HotelDetail.as_view(), name='hotel_detail'),
    path('', RegionList.as_view(), name='region'),
]