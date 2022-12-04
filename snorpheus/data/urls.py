from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # list collection periods and sessions for patient
    path(
        "patients/<int:patient_id>",
        views.get_patient_sessions,
        name="get_patient_sessions",
    ),
    # get data for one sleep session
    path(
        "sessions/<int:session_id>",
        views.get_session_data,
        name="get_session_data",
    ),
    # get data for one collection period
    path(
        "periods/<int:period_id>",
        views.get_period_data,
        name="get_period_data",
    ),
    # get combined position/audio data for one collection period
    path(
        "periods/<int:period_id>/joined",
        views.get_joined_period_data,
        name="get_joined_period_data",
    ),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
