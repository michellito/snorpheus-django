from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from snorpheus.data.models import Position
from snorpheus.portal.models import CollectionPeriod, Patient, SleepSession

# from django.shortcuts import get_object_or_404, render
# from django.views.decorators.csrf import csrf_exempt


# def index(request):
#     return render(request, 'index.html')


def get_session_position(request, session_id):

    position_data = [
        {
            "x": position_event.x,
            "y": position_event.y,
            "z": position_event.z,
            "position": position_event.position,
        }
        for position_event in Position.objects.filter(sleep_session_id=session_id)
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
                        "start_time": session.start_time,
                        "end_time": session.end_time,
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

    print(audio_files[0].__dict__)

    session_data = {
        "id": sleep_session.id,
        "start_time": sleep_session.start_time,
        "end_time": sleep_session.end_time,
        "position_data": [
            {
                "timestamp": event.timestamp,
                "position": event.position,
            }
            for event in sleep_session.positions.all()
        ],
        "audio_data": [
            {"start_time": audio.start_time, "audio_file": audio.audio_file.name}
            for audio in sleep_session.audio_files.all()
        ],
    }

    return JsonResponse(status=200, data=session_data, safe=False)
