from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'attraction'

urlpatterns = [
    path('<category_slug>/', AttractionList.as_view(), name='attraction_list' ),
    path('<category_slug>/<slug>/', AttractionDetail.as_view(), name='attraction_detail' ),
]
