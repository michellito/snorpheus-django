from django.db import models

from snorpheus.portal.models import SleepSession


class PositionEvent(models.Model):
    """A Collection Period occurs when a patient is assigned by the clinician
    to wear the device for one or more nights of sleep.
    """

    POSITION_CHOICES = [
        ("Supine", "Supine"),
        ("Prone", "Prone"),
        ("Left", "Left"),
        ("Right", "Right"),
        ("Standing", "Standing"),
        ("Other", "Other"),
    ]

    sleep_session = models.ForeignKey(
        SleepSession, on_delete=models.CASCADE, related_name="position_events"
    )

    timestamp = models.DateTimeField(blank=True, null=True)
    seconds_elapsed = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    angle = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    position = models.CharField(max_length=8, choices=POSITION_CHOICES, blank=True)

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Position Event"
        app_label = "data"
