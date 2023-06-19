from django.contrib import admin
from page.models import Page, StatusCode

class StatusCodeAdmin(admin.ModelAdmin):
    model = StatusCode
    list_display = ('title', 'h1', 'content_1',)
    ordering = ('title',)

admin.site.register(Page)
admin.site.register(StatusCode,StatusCodeAdmin)

