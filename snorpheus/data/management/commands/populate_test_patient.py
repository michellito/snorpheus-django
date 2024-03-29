import datetime
import zoneinfo
from random import randrange

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from snorpheus.portal.models import Patient, SleepSession, CollectionPeriod
from snorpheus.data.models import PositionEvent


class Command(BaseCommand):

    def handle(self, *args, **options):

        phx_tz = zoneinfo.ZoneInfo("America/Phoenix")

        new_patient, created = Patient.objects.get_or_create(
            first_name="Nirav",
            last_name="Merchant"
        )

        collection_period, created = CollectionPeriod.objects.get_or_create(
            patient=new_patient,
            start_date="2022-11-19",
            end_date="2022-11-22"
        )
        
        session_dates = [
            {
                'device_start_time': datetime.datetime(2022, 11, 19, 22, 30, tzinfo=phx_tz),
                'device_end_time': datetime.datetime(2022, 11, 20, 5, 25, tzinfo=phx_tz)
            },
            {
                'device_start_time': datetime.datetime(2022, 11, 20, 21, 15, tzinfo=phx_tz),
                'device_end_time': datetime.datetime(2022, 11, 21, 5, 9, tzinfo=phx_tz)
            },
        ]

        positions = ['Supine', 'Prone', 'Left', 'Right']

        for s in session_dates:

            new_sleep_session, created = SleepSession.objects.get_or_create(
                collection_period=collection_period,
                device_start_time=s['device_start_time'],
                device_end_time=s['device_end_time'],
            )

            current_seconds = 0

            # get random position for time 0 aand create PositionEvent
            position_index = randrange(4)
            position = positions[position_index]
            
            PositionEvent.objects.create(
                sleep_session=new_sleep_session,
                seconds_elapsed=current_seconds,
                position=position
            )

            session_duration_seconds = (s['device_end_time'] - s['device_start_time']).total_seconds()

            while current_seconds < session_duration_seconds:
                
                # get random position and minute elapsed since last event
                position_index = randrange(4)
                minutes_elapsed = randrange(10, 80)

                position = positions[position_index]
                current_seconds = current_seconds + (minutes_elapsed * 60)

                PositionEvent.objects.create(
                    sleep_session=new_sleep_session,
                    seconds_elapsed=current_seconds,
                    position=position
                )






        


        



