from django.contrib.auth.decorators import login_required
from django.urls import path

from hotel.models import BookmarkHotel
from hotel.views import BookmarkView, favorites_list, add_to_favorites, remove_from_favorites

app_name = 'hotel'

urlpatterns = [
    path('<id>/bookmark/', add_to_favorites, name='hotel_bookmark'),
    path('bookmarks/', favorites_list, name='bookmarks'),
]
