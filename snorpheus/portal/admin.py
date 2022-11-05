from django.contrib import admin

from .models import Clinician, CollectionPeriod, Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "first_name", "last_name")
    search_fields = ("patient_id", "first_name", "last_name")

    # def folder_display(self, obj):
    #     return ", ".join([
    #         folder.friendly_name for folder in obj.folders.all()
    #     ])

    # folder_display.short_description = "Folders"


class ClinicianAdmin(admin.ModelAdmin):
    list_display = ("clinician_id", "user")
    search_fields = ("clinician_id", "user")


class CollectionPeriodAdmin(admin.ModelAdmin):
    list_display = ("patient", "start_date", "end_date")
    search_fields = ("patient", "start_date", "end_date")


admin.site.register(Patient, PatientAdmin)
admin.site.register(Clinician, ClinicianAdmin)
admin.site.register(CollectionPeriod, CollectionPeriodAdmin)
