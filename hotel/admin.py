from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.loader import get_template

from hotel.forms import HotelAdminForm, NumberAdminForm
from hotel.models import *


class MyAdminSite(AdminSite):

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        # for app in app_list:
        #    app['models'].sort(key=lambda x: x['name'])

        return app_list


class TypeOfObjectAdmin(admin.ModelAdmin):
    model = TypeofObject
    prepopulated_fields = {"slug": ("title",)}


class HotelImageAdmin(admin.TabularInline):
    model = HotelPhoto
    extra = 3
    classes = ('collapse',)
    fields = ("showphoto_thumbnail",)
    readonly_fields = ("showphoto_thumbnail",)
    max_num = 0

    def showphoto_thumbnail(self, instance):
        """A (pseudo)field that returns an image thumbnail for a show photo."""

        tpl = get_template("hotel/admin_thumbnail.html")
        return tpl.render({"photo": instance.image})

    showphoto_thumbnail.short_description = "Thumbnail"


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
                formfield.queryset = formfield.queryset.filter(hotel__id=request.resolver_match.kwargs['object_id'])
            else:
                formfield.queryset = formfield.queryset.none()
        return formfield


class HotelAdmin(admin.ModelAdmin):
    form = HotelAdminForm
    inlines = [HotelImageAdmin, HotelDistanceAdmin, HotelPriceInline]
    list_filter = ('city',)
    list_display = ['title', 'city']
    fieldsets = (
        ('Мета описание', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Модерация', {
            'fields': ('published', 'premium')
        }),
        ('Основное', {
            'fields': (
                'pub_date', 'user', 'title', 'object_type', 'object_service', 'remoteness', 'beach', 'centr', 'options',
                'description', 'video')
        }),
        ('Адрес', {
            'fields': ('address', 'city')
        }),
        ('Правила', {
            'fields': (
                'prepayment', 'free_cancel', 'early_booking_discount', 'requisites', 'prepayments_term', 'minimum',
                'chek_in', 'chek_out', 'pets', 'child', 'another_rules')
        }),
        ('Мультизагрузка фотографий', {
            'fields': ('images',)
        }),

    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)


class NumberImageInline(admin.TabularInline):
    model = NumberPhoto
    extra = 3
    classes = ('collapse',)
    fields = ("showphoto_thumbnail",)
    readonly_fields = ("showphoto_thumbnail",)
    max_num = 0

    def showphoto_thumbnail(self, instance):
        """A (pseudo)field that returns an image thumbnail for a show photo."""

        tpl = get_template("hotel/admin_thumbnail.html")
        return tpl.render({"photo": instance.image})

    showphoto_thumbnail.short_description = "Thumbnail"


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
    form = NumberAdminForm
    inlines = [NumberImageInline]
    list_filter = ['hotel']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)

    def get_form(self, request, obj=None, **kwargs):
        request._place_obj = obj
        return super(NumberAdmin, self).get_form(request, obj, **kwargs)


class HotelPriceAdmin(admin.ModelAdmin):
    list_display = ['price', 'get_period', 'number', 'get_hotel']
    list_filter = ['period__hotel', ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)

    def get_period(self, obj):
        return obj.period

    def get_hotel(self, obj):
        return obj.period.hotel


class PricePeriodInline(admin.TabularInline):
    model = Price
    extra = 3
    classes = ('collapse',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super(PricePeriodInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'number':
            if request.resolver_match.kwargs['object_id'] is not None:
                period = PricePeriod.objects.get(id=request.resolver_match.kwargs['object_id'])
                formfield.queryset = formfield.queryset.filter(hotel__id=period.hotel.id)
            else:
                formfield.queryset = formfield.queryset.none()
        return formfield


class PricePeriodAdmin(admin.ModelAdmin):
    inlines = [PricePeriodInline]
    list_display = ['period', 'hotel']
    list_filter = ['hotel']

    def period(self, obj):
        return f'Период с {obj.start.strftime("%d-%m-%Y")} -  по {obj.end.strftime("%d-%m-%Y")}'


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(PricePeriod, PricePeriodAdmin)
admin.site.register(Price, HotelPriceAdmin)
admin.site.register(HotelOption)
admin.site.register(HotelContact)
admin.site.register(TypeofObject, TypeOfObjectAdmin)
admin.site.register(ServiceFilterofObject)
admin.site.register(NumberOption)
admin.site.register(Distance)
admin.site.register(DistanceTime)
