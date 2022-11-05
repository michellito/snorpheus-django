# from django.conf import settings
from django.db import models

from .people import Patient


class CollectionPeriod(models.Model):
    """ """

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="collection_period"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Collection Period"
        app_label = "portal"

    def __unicode__(self):
        return "Patient {}: {} - {}".format(
            self.patient.patient_id,
            self.start_date.strftime("%B %d, %Y"),
            self.end_date.strftime("%B %d, %Y"),
        )

    def __str__(self):
        return "Patient {}: {} - {}".format(
            self.patient.patient_id,
            self.start_date.strftime("%B %d, %Y"),
            self.end_date.strftime("%B %d, %Y"),
        )
