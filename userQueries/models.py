from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ApplicationForRegistration(models.Model):
   """Заявка для регистрации пользователей"""
   email = models.EmailField(verbose_name="Email", unique=True)
   phone = models.CharField(max_length=12, verbose_name='Телефон')
   create_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

   class Meta:
      verbose_name = 'Заявка для регистрации'
      verbose_name_plural = 'Заявки для регистрации'

   def __str__(self):
      return self.phone


class Feedback(models.Model):
   """Обратная связ"""
   name = models.CharField(max_length=100, verbose_name='Имя')
   phone = PhoneNumberField(verbose_name='Номер телефона')
   email = models.EmailField(verbose_name="Email")
   message = models.TextField(verbose_name='Сообщение')
   create_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

   class Meta:
      verbose_name = 'Запрос на обратную связ'
      verbose_name_plural = 'Запросы на обратную связ'

   def __str__(self):
      return self.name