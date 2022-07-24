from django.contrib import admin
from hotel.models import *


class TypeOfObjectAdmin(admin.ModelAdmin):
    model = TypeofObject
    prepopulated_fields = {"slug": ("title",)}


class HotelImageAdmin(admin.TabularInline):
    model = HotelPhoto
    extra = 3
    classes = ('collapse',)


class HotelDistanceAdmin(admin.TabularInline):
    model = DistanceTime
    extra = 3
    classes = ('collapse',)


class HotelNumberInline(admin.StackedInline):
    model = Number
    extra = 3
    classes = ('collapse',)


class HotelPriceInline(admin.TabularInline):
    model = PricePeriod
    extra = 3
    classes = ('collapse',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super(HotelPriceInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'number':
            if request.resolver_match.kwargs['object_id'] is not None:
                formfield.queryset = formfield.queryset.filter(hotel__id = request.resolver_match.kwargs['object_id'])
            else:
                formfield.queryset = formfield.queryset.none()
        return formfield

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageAdmin, HotelDistanceAdmin, HotelPriceInline]
    list_display = ['title', 'city']
    fieldsets = (
        ('Мета описание', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Основное', {
            'fields': ('premium','user', 'title', 'object_type','object_service', 'remoteness', 'beach', 'options', 'description', 'video')
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

# class NumberPriceInline(admin.TabularInline):
#     model = Price
#     extra = 3
#     classes = ('collapse',)
#
#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#
#         formfield = super(NumberPriceInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == 'period':
#             if request._place_obj is not None:
#                 formfield.queryset = formfield.queryset.filter(hotel = request._place_obj.hotel)
#             else:
#                 formfield.queryset = formfield.queryset.none()
#         return formfield

class NumberAdmin(admin.ModelAdmin):
    inlines = [NumberImageInline]
    list_filter = ['hotel']



    def get_form(self, request, obj=None, **kwargs):
        request._place_obj = obj
        return super(NumberAdmin, self).get_form(request, obj, **kwargs)


# class NumberPriceAdmin(admin.ModelAdmin):
#     list_display = ['price','get_period','number','get_hotel']
#     list_filter = ['period__hotel',]
#
#     def get_period(self, obj):
#         return obj.period
#
#     def get_hotel(self, obj):
#         return obj.period.hotel

class PricePeriodAdmin(admin.ModelAdmin):
    list_display = ['period', 'hotel']
    list_filter = ['hotel']

    def period(self, obj):
        return str(obj.start) + '/' + str(obj.end)





admin.site.register(Hotel, HotelAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(HotelOption)
admin.site.register(HotelContact)
admin.site.register(TypeofObject,TypeOfObjectAdmin)
admin.site.register(ServiceFilterofObject)
admin.site.register(NumberOption)
admin.site.register(Distance)
admin.site.register(DistanceTime)
admin.site.register(PricePeriod, PricePeriodAdmin)




