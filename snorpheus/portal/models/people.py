from django.conf import settings
from django.db import models


class Patient(models.Model):
    """ """

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Patient"
        app_label = "portal"

    def __unicode__(self):
        return "Patient {}: {} {}".format(
            self.id, self.first_name, self.last_name
        )

    def __str__(self):
        return "Patient {}: {} {}".format(
            self.id, self.first_name, self.last_name
        )


class Clinician(models.Model):
    """ """

    # Relationship Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clinician",
    )

    class Meta:
        verbose_name = "Clinician"
        app_label = "portal"

    def __unicode__(self):
        return f"Clinician {self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"Clinician {self.user.first_name} {self.user.last_name}"
