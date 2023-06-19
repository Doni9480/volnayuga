from django.contrib import admin
from userQueries.models import ApplicationForRegistration


class ApplicationForRegistrationAdmin(admin.ModelAdmin):
   model = ApplicationForRegistration
   list_display = ('phone', 'email', 'create_time',)
   search_fields = ('email', 'phone',)
   ordering = ('create_time', 'email',)


admin.site.register(ApplicationForRegistration, ApplicationForRegistrationAdmin)
