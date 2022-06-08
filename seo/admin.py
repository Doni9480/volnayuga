from django.contrib import admin
from .models import *


class SeoForTypeAdmin(admin.ModelAdmin):
    list_filter = ['city']

admin.site.register(SeoPage)
admin.site.register(SeoForType, SeoForTypeAdmin)
