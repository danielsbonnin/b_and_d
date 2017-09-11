from django.contrib import admin
from .models import Child, UpdateEvent, DailyRequirementsReport

class UpdateEventAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

class DailyRequirementsReportAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
# Register your models here.
admin.site.register(Child)
admin.site.register(UpdateEvent, UpdateEventAdmin)
admin.site.register(DailyRequirementsReport, DailyRequirementsReportAdmin)