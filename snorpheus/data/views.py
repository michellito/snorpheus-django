from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from snorpheus.data.models import PositionEvent, AudioLabel
from snorpheus.portal.models import CollectionPeriod, Patient, SleepSession

from django.core.cache import cache

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
        patient = Patient.objects.get(id=patient_id)
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
                        "id": session.id,
                        "device_start_time": session.device_start_time,
                        "device_end_time": session.device_end_time,
                        "true_start_time": session.true_start_time
                    }
                    for session in period.get_sleep_sessions().order_by('device_start_time')
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
        "device_start_time": sleep_session.device_start_time,
        "position_events": [
            {
                "seconds_elapsed": event.seconds_elapsed,
                "position": event.position,
            }
            for event in sleep_session.position_events.all().order_by('seconds_elapsed')
        ],
        "audio_labels": audio_labels,
    }

    return JsonResponse(status=200, data=session_data, safe=False)


def get_period_data(request, period_id):

    reload_cache = request.GET.get('reload_cache', "")
    period_data = cache.get('period:%s' % period_id)
    
    if reload_cache == 'true' or not period_data:
        
        period_data = []
        period = CollectionPeriod.objects.get(id=period_id)
        
        for sleep_session in period.sleep_sessions.all():

            print(sleep_session)

            audio_labels = []
            position_events = sleep_session.position_events.all().order_by('seconds_elapsed')
            position_events_list = list(position_events)


            for audio_file in sleep_session.audio_files.all():

                last_position_index = 0
                last_position = position_events_list[0].position

                for label in audio_file.labels.all():

                    timestamp_seconds = audio_file.seconds_elapsed + label.seconds_elapsed
                    if timestamp_seconds > position_events_list[last_position_index + 1].seconds_elapsed:
                        position = position_events_list[last_position_index + 1].position
                        last_position_index += 1
                    else:
                        position = last_position
                    
                    audio_labels.append(
                        {
                            "timestamp_seconds": timestamp_seconds,
                            "seconds_elapsed": label.seconds_elapsed,
                            "label_1": label.label_1,
                            "label_2": label.label_2,
                            "label_3": label.label_3,
                            "audio_file": audio_file.audio_file.name,
                            "audio_start_time": audio_file.start_time,
                            "position": position
                        }
                    )

            period_data.append({
                "id": sleep_session.id,
                "device_start_time": sleep_session.device_start_time,
                "device_end_time": sleep_session.device_end_time,
                "position_events": [
                    {
                        "seconds_elapsed": event.seconds_elapsed,
                        "position": event.position,
                    }
                    for event in position_events
                ],
                "audio_labels": audio_labels,
            })

        cache.set(
            'period:%s' % period_id,
            period_data,
            timeout=None
        )


    return JsonResponse(status=200, data=period_data, safe=False)


def get_joined_period_data(request, period_id):

    period_data = []
    period = CollectionPeriod.objects.get(id=period_id)
    
    for sleep_session in period.sleep_sessions.all():
        
        audio_labels = AudioLabel.objects.filter(audio_file__sleep_session__id=sleep_session.id)
        audio_labels_list = list(audio_labels)

        if len(audio_labels_list):
            print(audio_labels_list[0].total_seconds_elapsed)
            
        
        # # get session duration
        # duration_seconds = (sleep_session.device_end_time - sleep_session.device_start_time).total_seconds()
        # print(duration_seconds)

        # f

        # # for each second, get sound and position
        # for s in range(0, duration_seconds, 1):
        #     # get audio events between [s, s+1]
            

    return JsonResponse(status=200, data=period_data, safe=False)
