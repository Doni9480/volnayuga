from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'verificated']


admin.site.register(Review, ReviewAdmin)

