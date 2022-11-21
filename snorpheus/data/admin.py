from django.contrib import admin

from .models import AudioLabel, Position, SleepSessionAudio, SnoringEpisode


class SleepSessionAudioAdmin(admin.ModelAdmin):
    list_display = ("id", "sleep_session", "audio_file", "start_time")
    search_fields = ("sleep_session", "audio_file")


class SnoringEdpisodeAdmin(admin.ModelAdmin):
    list_display = ("id", "sleep_session", "start_time", "end_time")
    search_fields = ("sleep_session",)


class AudioLabelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "audio_file",
        "timestamp",
        "label_1",
        "label_2",
        "label_3",
        "score_1",
        "score_2",
        "score_3",
    )


class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "x", "y", "z", "angle", "position")


admin.site.register(SleepSessionAudio, SleepSessionAudioAdmin)
admin.site.register(SnoringEpisode, SnoringEdpisodeAdmin)
admin.site.register(AudioLabel, AudioLabelAdmin)
admin.site.register(Position, PositionAdmin)
