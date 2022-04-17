import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms

from accounts.forms import HotelOptionForm
from hotel.models import Hotel, HotelOption, TypeofObject


class ProductFilter(django_filters.FilterSet):

      class Meta:
          form = HotelOptionForm




