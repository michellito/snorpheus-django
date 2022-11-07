# from django.core.files.storage import FileSystemStorage
from django.db import models

from snorpheus.portal.models import SleepSession

# fs = FileSystemStorage(location='/media/audio')


class SleepSessionAudio(models.Model):
    """A Collection Period occurs when a patient is assigned by the clinician
    to wear the device for one or more nights of sleep.
    """

    sleep_session = models.ForeignKey(
        SleepSession, on_delete=models.CASCADE, related_name="sleep_session"
    )

    start_time = models.DateTimeField()
    audio_file = models.FileField(upload_to="audio/")

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Sleep Session Audio"
        app_label = "data"

    def __str__(self):
        return self.sleep_session.__str__()
