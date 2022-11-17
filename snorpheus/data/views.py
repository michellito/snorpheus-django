from django.http import JsonResponse

from snorpheus.data.models import Position
from snorpheus.portal.models import CollectionPeriod, SleepSession

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

    collection_periods = CollectionPeriod.objects.filter(patient_id=patient_id)
    period_data = []

    for period in collection_periods:
        period_data.append(
            {
                "start_date": period.start_date,
                "end_date": period.end_date,
                "sleep_sessions": [
                    {"start_time": session.start_time, "end_time": session.end_time}
                    for session in period.get_sleep_sessions()
                ],
            }
        )

    return JsonResponse(status=200, data=period_data, safe=False)


def get_session_data(request, period_id):

    sleep_sessions = SleepSession.objects.filter(collection_period_id=period_id)

    session_data = []

    for session in sleep_sessions:
        session_data.append(
            {
                "start_time": session.start_time,
                "end_time": session.end_time,
            }
        )
