from django.contrib import admin
from .models import *

# Register your models here.
class GalleryRegionInline(admin.TabularInline):
    model = GalleryForRegion
    extra = 3

class GalleryRegionAdmin(admin.ModelAdmin):
    inlines = [GalleryRegionInline]
    list_display = ['title', 'parent']

admin.site.register(Region, GalleryRegionAdmin)