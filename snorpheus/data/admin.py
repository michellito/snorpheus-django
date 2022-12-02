from django.contrib import admin

from .models import AudioLabel, PositionEvent, AudioFile, SnoringEpisode


class AudioFileAdmin(admin.ModelAdmin):
    list_display = ("id", "sleep_session", "audio_file", "start_time", "seconds_elapsed")
    search_fields = ("sleep_session", "audio_file")


class SnoringEpisodeAdmin(admin.ModelAdmin):
    list_display = ("id", "sleep_session", "start_seconds_elapsed", "end_seconds_elapsed")
    search_fields = ("sleep_session",)


class AudioLabelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "audio_file",
        "seconds_elapsed",
        "label_1",
        "label_2",
        "label_3",
    )


class PositionEventAdmin(admin.ModelAdmin):
    list_display = ("id", "sleep_session", "timestamp", "seconds_elapsed", "angle", "position")


admin.site.register(AudioFile, AudioFileAdmin)
admin.site.register(SnoringEpisode, SnoringEpisodeAdmin)
admin.site.register(AudioLabel, AudioLabelAdmin)
admin.site.register(PositionEvent, PositionEventAdmin)
