from django.http import JsonResponse

from snorpheus.data.models import Position

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
