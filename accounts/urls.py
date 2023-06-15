from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('application_registration/', application_for_registration, name="application_registration"),
    # path('register/', register_request, name="register"),
    path('login/', login_request, name="login"),
    path('logout/', logout_request, name= "logout"),
    path('password_reset/', password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('lk/', HotelList.as_view(), name='user_hotel_list'),
    path('lk/create_hotel/', HotelCreate.as_view(), name='hotel_create'),
    path('lk/<int:pk>/delete/', HotelDelete.as_view(), name='hotel_delete'),
    path('lk/<int:pk>/update/', HotelUpdate.as_view(), name='hotel_update'),
    path('lk/<int:pk>/info/', HotelDetail.as_view(), name='user_hotel_detail'),
    path('lk/<int:pk>/priceperiod/', HotelPricePeriodUpdate.as_view(), name='user_hotel_price_period_update'),
    path('lk/<int:pk>/priceperiod_delete/', price_period_delete, name='user_hotel_price_period_delete'),
    path('lk/priceupdate/', price_update, name='price_update'),
    path('lk/<int:pk>/<int:photo_pk>/delete/', HotelPhotoDelete.as_view(), name='hotel_photo_delete'),
    path('lk/<int:pk>/rules/', HotelRules.as_view(), name='hotel_rules'),
    path('lk/<int:hotel_pk>/number_create/', NumberCreate.as_view(), name='number_create'),
    path('lk/<int:pk>/image_upload/', number_image_upload, name='number_image_upload'),
    path('lk/<int:pk>/hotel_image_upload/', hotel_image_upload, name='hotel_image_upload'),
    path('lk/<int:pk>/hotel_image_delete/', hotel_image_delete, name='hotel_image_delete'),
    path('lk/<int:hotel_pk>/<int:pk>/number_update/', NumberUpdate.as_view(), name='number_update'),
    path('lk/<int:hotel_pk>/<int:pk>/number_delete/', NumberDelete.as_view(), name='number_delete'),
    path('lk/<int:image_pk>/number_image_delete/', number_image_delete, name='number_image_delete'),
    path('lk/<int:hotel_pk>/contact_create/', ContactCreate.as_view(), name='contact_create'),
    path('lk/<int:hotel_pk>/<int:pk>/', ContactUpdate.as_view(), name='contact_update'),
    path('lk/<int:hotel_pk>/<int:pk>/delete', ContactDelete.as_view(), name='contact_delete'),
    path('lk/<int:hotel_pk>/options_update/', HotelOptionUpdate.as_view(), name='hotel_options_update'),
    path('lk/<int:hotel_pk>/distance_add/', DistanceAdd.as_view(), name='hotel_distance_add'),
    path('lk/<int:hotel_pk>/<pk>/distance_delete/', DistanceDelete.as_view(), name='hotel_distance_delete'),
    path('lk/reviewlist/', HotelReviewList.as_view(), name='hotel_review_list'),
    path('lk/help/', HotelHelp.as_view(), name='hotel_help'),



]
