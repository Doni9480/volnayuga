from django.contrib import admin
from userQueries.models import ApplicationForRegistration, Feedback


class ApplicationForRegistrationAdmin(admin.ModelAdmin):
   model = ApplicationForRegistration
   list_display = ('phone', 'email', 'create_time',)
   search_fields = ('email', 'phone',)
   ordering = ('create_time', 'email',)


class FeedbackAdmin(admin.ModelAdmin):
   model = Feedback
   list_display = ('name', 'phone', 'email', 'message', 'create_time',)
   search_fields = ('name', 'email', 'phone', 'message',)
   ordering = ('create_time',)


admin.site.register(ApplicationForRegistration, ApplicationForRegistrationAdmin)
admin.site.register(Feedback, FeedbackAdmin)