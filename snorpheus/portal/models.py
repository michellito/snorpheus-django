from django.conf import settings
from django.db import models


class Patient(models.Model):
    """ """

    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, required=False)
    last_name = models.CharField(max_length=50, required=False)

    class Meta:
        verbose_name = "Patient"

    def __unicode__(self):
        return "Patient %s" % self.patient_id

    def __str__(self):
        return self.patient_id


class Clinician(models.Model):
    """ """

    clinician_id = models.AutoField(primary_key=True)

    # Relationship Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clinician",
    )

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Clinician"

    def __unicode__(self):
        return f"Clinician {self.user.first_name} {self.user.last_name}"


class CollectionPeriod(models.Model):
    """ """

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="collection_period"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ("-pk",)
        verbose_name = "Collection Period"

    def __unicode__(self):
        return "Patient %s" % self.pk

    def __str__(self):
        return self.user.first_name
