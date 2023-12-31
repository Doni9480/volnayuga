from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'
    verbose_name = 'Гостиницы и номера'

    def ready(self):
        import hotel.signals
