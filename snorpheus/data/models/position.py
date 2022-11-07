from django.db import models

from snorpheus.portal.models import SleepSession


class Position(models.Model):
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
        SleepSession, on_delete=models.CASCADE, related_name="positions"
    )

    timestamp = models.DateTimeField()
    x = models.DecimalField(max_digits=5, decimal_places=2)
    y = models.DecimalField(max_digits=5, decimal_places=2)
    z = models.DecimalField(max_digits=5, decimal_places=2)

    angle = models.DecimalField(max_digits=5, decimal_places=2)
    position = models.CharField(max_length=8, choices=POSITION_CHOICES, blank=True)

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Position"
        app_label = "data"
