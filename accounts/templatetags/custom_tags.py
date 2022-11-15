from django import template
from hotel.models import Price

register = template.Library()


@register.simple_tag
def price_tag(number, period):
    price = Price.objects.filter(number_id=number, period_id=period)
    return price
