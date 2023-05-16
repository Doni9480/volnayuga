from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from hotel.models import Hotel
from region.models import Region
from review.forms import ReviewForm
from review.models import Review


class ReviewAddView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review-create.html'
    success_url = '/'

    def form_valid(self, form):
        review = form.save(commit=False)
        hotel = Hotel.objects.get(id=self.request.POST['hotel'])
        city = Region.objects.get(slug=self.request.POST['region'])
        email = self.request.POST['email']
        review.hotel = hotel
        review.city = city
        review.email = email
        review.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


