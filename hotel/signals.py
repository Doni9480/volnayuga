from django.db.models.signals import post_save
from django.dispatch import receiver

from hotel.models import PricePeriod, Price, Number, Hotel
from django.core.mail import mail_admins, send_mail
from django.contrib.sites.models import Site
# from VolnaYuga.settings import 


@receiver(post_save, sender=PricePeriod)
def create_price_for_period(sender, instance, created, **kwargs):
    if created:
        number_list = Number.objects.filter(hotel=instance.hotel)
        for number in number_list:
            Price.objects.create(price='0', period=instance, number=number)
            
    
@receiver(post_save, sender=Hotel)
def send_notification(sender, instance, created, **kwargs):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    if created:
        subject = 'На сайте ВашеМоре.Ру добавлен новый объект'
        message = f'На сайте ВашеМоре.Ру добавлен новый объект от пользователя {instance.user}. Модерация {domain}/hotel/hotel/{instance.pk}change/'
        mail_admins(
            subject=subject,
            message=message,
        )
    if not created and instance.published:
        subject = 'Ваше объявление опубликовано - ВашеМоре.Ру'
        message = f'Уважаемый {instance.user}, ваше объявление опубликовано на сайте {domain}/{instance.city.slug}/{instance.pk}'
        recipient = instance.user
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=(recipient,)
        )
        