from django.contrib import admin

from .models import Clinician, CollectionPeriod, Patient, SleepSession


class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("id", "first_name", "last_name")

    # def folder_display(self, obj):
    #     return ", ".join([
    #         folder.friendly_name for folder in obj.folders.all()
    #     ])

    # folder_display.short_description = "Folders"


class ClinicianAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("id", "user")


class CollectionPeriodAdmin(admin.ModelAdmin):
    list_display = ("patient", "start_date", "end_date")
    search_fields = ("patient", "start_date", "end_date")


class SleepSessionAdmin(admin.ModelAdmin):
    list_display = ("collection_period", "device_start_time", "device_end_time", "true_start_time")
    search_fields = ("collection_period", "device_start_time", "device_end_time", "true_start_time")


admin.site.register(Patient, PatientAdmin)
admin.site.register(Clinician, ClinicianAdmin)
admin.site.register(CollectionPeriod, CollectionPeriodAdmin)
admin.site.register(SleepSession, SleepSessionAdmin)
