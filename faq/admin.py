from django.contrib import admin
from faq.models import Faq

class FaqAdmin(admin.ModelAdmin):
    model = Faq
    list_display = ('question', 'sorting', 'answer',)
    list_filter = ('question',)
    search_fields = ('question',)
    ordering = ('sorting', 'question',)
    list_editable = ('sorting',)


admin.site.register(Faq, FaqAdmin)

