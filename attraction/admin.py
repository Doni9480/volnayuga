from django.contrib import admin
from .models import *

# Register your models here.

class AtrractionAdminInline(admin.TabularInline):
    model = AttractionGallery
    extra = 3

class AttributeAdmin(admin.ModelAdmin):
    inlines = [AtrractionAdminInline, ]

admin.site.register(AttractionCategory)
admin.site.register(Attraction, AttributeAdmin)