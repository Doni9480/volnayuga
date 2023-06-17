from django.db import models


class ApplicationForRegistration(models.Model):
   """Заявка для регистрации пользователей"""
   email = models.EmailField(verbose_name="Email", unique=True)
   phone = models.CharField(max_length=12, verbose_name='Телефон')
   create_time = models.DateTimeField(
      auto_now_add=True, verbose_name="Время создания")

   class Meta:
      verbose_name = 'Заявка для регистрации'
      verbose_name_plural = 'Заявки для регистрации'

   def __str__(self):
      return self.phone
