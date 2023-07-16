from django.db import models


class Faq(models.Model):
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    sorting = models.PositiveIntegerField(default=0, verbose_name='Сортировка (порядок вывода на сайт)')
    

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"

    def __str__(self):
        return self.question
