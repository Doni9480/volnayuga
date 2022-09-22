from django.urls import path
from .views import PageDetail


app_name = 'page'

urlpatterns = [
    path('<slug:slug>/', PageDetail.as_view(), name='page_detail'),
]
