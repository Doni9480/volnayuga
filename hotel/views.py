from django.shortcuts import render
from django.views.generic import DetailView, ListView

from review.models import Review
from .models import Hotel
from region.models import Region


def home_view(request):
    region_list = Region.objects.filter(parent=None)
    review_list = Review.objects.filter(verificated=True)
    region_popular_list = Region.objects.filter(is_popular=True)
    context = {
        'region_list':region_list,
        'region_popular_list':region_popular_list,
        'review_list':review_list,
    }
    return render(request, template_name='hotel/home.html', context=context)





