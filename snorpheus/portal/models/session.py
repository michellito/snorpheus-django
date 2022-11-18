# from django.conf import settings
from django.db import models

from .people import Patient


class CollectionPeriod(models.Model):
    """A Collection Period occurs when a patient is assigned by the clinician
    to wear the device for one or more nights of sleep.
    """

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Collection Period"
        app_label = "portal"

    def get_sleep_sessions(self):
        return self.sleep_sessions.all()

    def __unicode__(self):
        return "{} {}: {} - {}".format(
            self.patient.first_name,
            self.patient.last_name,
            self.start_date.strftime("%B %d, %Y"),
            self.end_date.strftime("%B %d, %Y"),
        )

    def __str__(self):
        return "{} {}: {} - {}".format(
            self.patient.first_name,
            self.patient.last_name,
            self.start_date.strftime("%B %d, %Y"),
            self.end_date.strftime("%B %d, %Y"),
        )


class SleepSession(models.Model):
    """A Sleep Session refers to one night of sleep within a
    Collection Period. One Collection Period may include multiple
    Sleep Sessions.
    """

    collection_period = models.ForeignKey(
        CollectionPeriod, on_delete=models.CASCADE, related_name="sleep_sessions"
    )

    # start/end time according to device
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # device time may be unreliable, allow patient to specify true start time
    true_start_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Sleep Session"
        app_label = "portal"

    def __str__(self):
        return "Sleep Session {}: {} - {}".format(
            self.id,
            self.start_time.strftime("%d-%m-%Y %H:%M"),
            self.end_time.strftime("%d-%m-%Y %H:%M"),
        )
