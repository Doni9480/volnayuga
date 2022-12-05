from django import template

from hotel.models import TypeofObject, Hotel

register = template.Library()

@register.filter()
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.simple_tag()
def get_type_of_object(value):
    hotel_list = Hotel.objects.filter(city=value)
    type_of_object_list = {}
    for item in hotel_list:
        for object_type in item.object_type.all():
            if object_type not in type_of_object_list:
                type_of_object_list[object_type] = object_type
                type_of_object_list[object_type] = object_type.hotel_set.all().count()
    return type_of_object_list
