from django.contrib import admin

from .models import Position, SleepSessionAudio, SnoringEpisode


class SleepSessionAudioAdmin(admin.ModelAdmin):
    list_display = ("sleep_session", "audio_file", "start_time")
    search_fields = ("sleep_session", "audio_file")


class SnoringEdpisodeAdmin(admin.ModelAdmin):
    list_display = ("sleep_session", "start_time", "end_time")
    search_fields = ("sleep_session",)


class PositionAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "x", "y", "z", "angle", "position")


admin.site.register(SleepSessionAudio, SleepSessionAudioAdmin)
admin.site.register(SnoringEpisode, SnoringEdpisodeAdmin)
admin.site.register(Position, PositionAdmin)
