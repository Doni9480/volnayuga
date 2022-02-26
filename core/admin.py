from django.contrib import admin
from core.models import *

class HotelImageDetail(admin.TabularInline):
    model = Photo_in_filter
    extra = 3

class HotelImagePage(admin.TabularInline):
    model = Photo_on_detail
    extra = 3

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImagePage, HotelImageDetail]

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Number)
admin.site.register(Hotel_option)
admin.site.register(Hotel_contact)
admin.site.register(Type_of_Object)
admin.site.register(Number_option)

