from django.urls import path, include
from region.views import HotelDetail
from region.views import RegionDetail

app_name = 'region'

urlpatterns = [
    path('', RegionDetail.as_view(), name='region_detail'),
    path('<pk>/', HotelDetail.as_view(), name='hotel_detail'),
]