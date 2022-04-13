from django.contrib import admin
from hotel.models import *


class HotelImageAdmin(admin.TabularInline):
    model = HotelPhoto
    extra = 3
    classes = ('collapse',)

class HotelDistanceAdmin(admin.TabularInline):
    model = DistanceTime
    extra = 3
    classes = ('collapse',)

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageAdmin, HotelDistanceAdmin]
    list_display = ['title', 'city']
    fieldsets = (
        ('Мета описание', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Основное', {
            'fields': ('premium','user', 'title', 'object_type', 'remoteness', 'beach', 'options', 'description', 'video')
        }),
        ('Адрес', {
            'fields': ('address', 'city')
        }),
        ('Правила', {
            'fields': ('prepayment', 'free_cancel', 'early_booking_discount', 'requisites', 'prepayments_term', 'minimum', 'chek_in', 'chek_out', 'pets', 'child', 'another_rules')
        }),

    )

class NumberImageInline(admin.TabularInline):
    model = NumberPhoto
    extra = 3
    classes = ('collapse',)

class NumberPriceInline(admin.TabularInline):
    model = Price
    extra = 3
    classes = ('collapse',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        formfield = super(NumberPriceInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'period':
            if request._place_obj is not None:
                formfield.queryset = formfield.queryset.filter(hotel = request._place_obj.hotel)
            else:
                formfield.queryset = formfield.queryset.none()
        return formfield

class NumberAdmin(admin.ModelAdmin):
    inlines = [NumberImageInline, NumberPriceInline]
    list_filter = ['hotel']



    def get_form(self, request, obj=None, **kwargs):
        request._place_obj = obj
        return super(NumberAdmin, self).get_form(request, obj, **kwargs)


class NumberPriceAdmin(admin.ModelAdmin):
    list_display = ['price','get_period','number','get_hotel']
    list_filter = ['number__hotel',]

    def get_period(self, obj):
        return obj.period

    def get_hotel(self, obj):
        return obj.number.hotel


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(HotelOption)
admin.site.register(HotelContact)
admin.site.register(TypeofObject)
admin.site.register(NumberOption)
admin.site.register(Distance)
admin.site.register(DistanceTime)
admin.site.register(Price, NumberPriceAdmin)
admin.site.register(PricePeriod)




