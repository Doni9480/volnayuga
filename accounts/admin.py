from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, ApplicationForRegistration

class CustomUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('name','phone','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class ApplicationForRegistrationAdmin(admin.ModelAdmin):
    model = ApplicationForRegistration
    list_display = ('phone', 'email', 'create_time',)
    search_fields = ('email', 'phone',)
    ordering = ('create_time', 'email',)

admin.site.register(MyUser, CustomUserAdmin)
admin.site.register(ApplicationForRegistration, ApplicationForRegistrationAdmin)
