from django import template
from collections import Counter

from hotel.forms import SearchHotelForm
from hotel.models import TypeofObject, Hotel

register = template.Library()


@register.filter()
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter()
def hotel_search_form():
    return SearchHotelForm()


@register.simple_tag()
def get_type_of_object(value):
    hotel_list = Hotel.objects.filter(city=value)
    type_of_object_list = []
    for item in hotel_list:
        for object_type in item.object_type.all():
            type_of_object_list.append(object_type)
    counter = {}
    for elem in type_of_object_list:
        counter[elem] = counter.get(elem, 0) + 1
    doubles = {element: count for element, count in counter.items() if count > 1}
    return counter
