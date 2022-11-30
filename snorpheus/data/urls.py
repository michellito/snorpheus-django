from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path(
        "sessions/<int:session_id>/position",
        views.get_session_data,
        name="get_session_data",
    ),
    path(
        "periods/<int:period_id>",
        views.get_period_sessions,
        name="get_period_sessions",
    ),
    path(
        "patients/<int:patient_id>",
        views.get_patient_sessions,
        name="get_patient_sessions",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
