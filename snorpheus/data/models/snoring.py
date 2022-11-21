from django.db import models

from snorpheus.portal.models import SleepSession


class SleepSessionAudio(models.Model):
    """A Collection Period occurs when a patient is assigned by the clinician
    to wear the device for one or more nights of sleep.
    """

    sleep_session = models.ForeignKey(
        SleepSession, on_delete=models.CASCADE, related_name="audio_files"
    )

    start_time = models.DateTimeField()
    audio_file = models.FileField(upload_to="audio/")

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Sleep Session Audio File"
        app_label = "data"

    def __str__(self):
        return self.sleep_session.__str__()


class SnoringEpisode(models.Model):

    sleep_session = models.ForeignKey(
        SleepSession, on_delete=models.CASCADE, related_name="snoring_episode"
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = "Snoring Episode"
        app_label = "data"

    def __str__(self):
        return f"{self.sleep_session.__str__()}: Episode {self.id}"


class AudioLabel(models.Model):

    audio_file = models.ForeignKey(
        SleepSessionAudio, on_delete=models.CASCADE, related_name="labels"
    )

    timestamp = models.DecimalField(max_digits=10, decimal_places=2)

    label_1 = models.CharField(max_length=50)
    label_2 = models.CharField(max_length=50)
    label_3 = models.CharField(max_length=50)

    score_1 = models.DecimalField(max_digits=5, decimal_places=3)
    score_2 = models.DecimalField(max_digits=5, decimal_places=3)
    score_3 = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        verbose_name = "Audio Label"
        app_label = "data"

    # def __str__(self):
    #     return f"{self.sleep_session.__str__()}: Episode {self.id}"
