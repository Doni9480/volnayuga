from django.db.models.signals import post_save
from django.dispatch import receiver

from hotel.models import PricePeriod, Price, Number


@receiver(post_save, sender=PricePeriod)
def create_price_for_period(sender, instance, created, **kwargs):
    if created:
        number_list = Number.objects.filter(hotel=instance.hotel)
        for number in number_list:
            Price.objects.create(price='0', period=instance, number=number)