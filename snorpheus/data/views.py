from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from snorpheus.data.models import PositionEvent
from snorpheus.portal.models import CollectionPeriod, Patient, SleepSession

# from django.shortcuts import get_object_or_404, render
# from django.views.decorators.csrf import csrf_exempt

# def index(request):
#     return render(request, 'index.html')


def get_session_position(request, session_id):

    position_data = [
        {
            "seconds_elapsed": position_event.seconds_elapsed,
            "angle": position_event.angle,
            "position": position_event.position,
        }
        for position_event in PositionEvent.objects.filter(sleep_session_id=session_id)
    ]

    return JsonResponse(status=200, data=position_data, safe=False)


def get_patient_sessions(request, patient_id):

    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=500, data={"error": "No patient found with this ID."}, safe=False
        )

    collection_periods = CollectionPeriod.objects.filter(patient_id=patient_id)
    period_data = []

    for period in collection_periods:
        period_data.append(
            {
                "start_date": period.start_date,
                "end_date": period.end_date,
                "sleep_sessions": [
                    {
                        "session_id": session.id,
                        "device_start_time": session.device_end_time,
                        "device_end_time": session.device_end_time,
                        "true_start_time": session.true_start_time
                    }
                    for session in period.get_sleep_sessions()
                ],
            }
        )

    response = {
        "patient_name": patient.first_name + " " + patient.last_name,
        "collection_periods": period_data,
    }

    return JsonResponse(status=200, data=response, safe=False)


def get_session_data(request, session_id):

    sleep_session = SleepSession.objects.get(id=session_id)
    audio_files = sleep_session.audio_files.all()

    audio_labels = []

    for audio_file in audio_files:
        for label in audio_file.labels.all():
            audio_labels.append(
                {
                    "timestamp_seconds": audio_file.seconds_elapsed + label.seconds_elapsed,
                    "seconds_elapsed": label.seconds_elapsed,
                    "label_1": label.label_1,
                    "label_2": label.label_2,
                    "label_3": label.label_3,
                    "audio_file": audio_file.audio_file.name,
                    "audio_start_seconds_elapsed": audio_file.seconds_elapsed
                }
            )

    session_data = {
        "id": sleep_session.id,
        "start_time": sleep_session.device_start_time,
        "position_events": [
            {
                "seconds_elapsed": event.seconds_elapsed,
                "position": event.position,
            }
            for event in sleep_session.position_events.all()
        ],
        "audio_labels": audio_labels,
    }

    return JsonResponse(status=200, data=session_data, safe=False)


def get_period_data(request, period_id):

    period_data = []
    period = CollectionPeriod.objects.get(id=period_id)
    
    for sleep_session in period.sleep_sessions.all():

        audio_labels = []

        for audio_file in sleep_session.audio_files.all():

            for label in audio_file.labels.all():
                audio_labels.append(
                    {
                        "timestamp_seconds": audio_file.seconds_elapsed + label.seconds_elapsed,
                        "seconds_elapsed": label.seconds_elapsed,
                        "label_1": label.label_1,
                        "label_2": label.label_2,
                        "label_3": label.label_3,
                        "audio_file": audio_file.audio_file.name,
                        "audio_start_time": audio_file.start_time
                    }
                )

        period_data.append({
            "id": sleep_session.id,
            "start_time": sleep_session.device_start_time,
            "position_events": [
                {
                    "seconds_elapsed": event.seconds_elapsed,
                    "position": event.position,
                }
                for event in sleep_session.position_events.all()
            ],
            "audio_labels": audio_labels,
        })

    return JsonResponse(status=200, data=period_data, safe=False)
