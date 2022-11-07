from django.contrib import admin

from .models import SleepSessionAudio


class SleepSessionAudioAdmin(admin.ModelAdmin):
    list_display = ("sleep_session", "audio_file", "start_time")
    search_fields = ("sleep_session", "audio_file", "start_time")


admin.site.register(SleepSessionAudio, SleepSessionAudioAdmin)
