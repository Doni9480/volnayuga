from django.contrib import admin
from .models import *

# Register your models here.
class GalleryRegionInline(admin.TabularInline):
    model = GalleryForRegion
    extra = 3
    classes = ('collapse',)

class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [GalleryRegionInline]
    list_display = ['title', 'parent', 'is_city', 'is_most_interesting', 'is_popular']
    list_editable = ['is_city', 'is_most_interesting', 'is_popular']
    list_filter = ['parent','is_popular', 'is_most_interesting']
    fieldsets = (
        ('Мета описание', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Основное', {
            'fields': ('title','slug','is_city', 'is_popular', 'is_most_interesting', 'image', 'parent', 'description', 'season')
        }),

    )

admin.site.register(Region, RegionAdmin)