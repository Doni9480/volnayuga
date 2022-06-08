from django.contrib import admin
from .models import *

class StaticDataAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        base_add_permission = super(StaticDataAdmin, self).has_add_permission(request)
        if base_add_permission:
            # if there's already an entry, do not allow adding
            count = StaticData.objects.all().count()
            if count == 0:
                return True
        return False

admin.site.register(StaticData, StaticDataAdmin)
