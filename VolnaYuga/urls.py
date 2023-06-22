"""VolnaYuga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from accounts.views import login_request, logout_request, password_reset_request
from core.sitemaps import HotelSitemap, RegionSitemap
from core.views import AboutPage, ContactPage, RentPage, HomePage
from django.conf import settings
from django.conf.urls.static import static

from hotel.models import Hotel
from region.views import RegionAutocomplete, HotelSearchBlock
from django.conf.urls import handler404


sitemaps = {
    'hotel': HotelSitemap,
    'region': RegionSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'city-autocomplete/',
        RegionAutocomplete.as_view(),
        name='city-autocomplete',
    ),
    path('search/', HotelSearchBlock.as_view(), name='hotel_search_block'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), ),
    path('about/', AboutPage.as_view(), name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('rent/', RentPage.as_view(), name='rent'),
    path('page/', include('page.urls', namespace='page')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('user_queries/', include('userQueries.urls', namespace='userQueries')),
    # path('register/', register_request, name="register"),
    path('login/', login_request, name="login_s"),
    path('logout/', logout_request, name="logout_s"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('<region_slug>/attraction/', include('attraction.urls', namespace='attraction')),
    path('review/', include('review.urls', namespace='review')),
    path('booking/', include('booking.urls', namespace='booking')),
    path('<slug>/', include('region.urls', namespace='region')),
    path('', HomePage.as_view(), name='home'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
