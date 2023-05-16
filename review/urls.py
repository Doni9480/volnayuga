from django.urls import path

from review.views import ReviewAddView

app_name = 'review'

urlpatterns = [
    path('create/', ReviewAddView.as_view(), name='review_add'),
]