import os
import pathlib

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from snorpheus.portal.models import Patient, SleepSession
from snorpheus.data.models import AudioFile


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("directory", nargs=1, type=str)
        parser.add_argument("audio_length_seconds", nargs=1, type=int)
        parser.add_argument("patient_id", nargs=1, type=int)
        parser.add_argument("session_id", nargs=1, type=int)

    def handle(self, *args, **options):

        directory = options["directory"][0]
        audio_length_seconds = options["audio_length_seconds"][0]
        patient_id = options["patient_id"][0]
        session_id = options["session_id"][0]

        try:
            patient = Patient.objects.get(id=patient_id)
        except ObjectDoesNotExist:
            raise CommandError('No patient found with ID "%s".' % patient_id)

        try:
            sleep_session = SleepSession.objects.get(id=session_id)
        except ObjectDoesNotExist:
            raise CommandError("No sleep session found with ID %s." % session_id)
        
        
        print("SleepSession: ", sleep_session)
        print("Patient: ", patient)
        print("directory: ", directory)
        print("audio_length_seconds: ", audio_length_seconds)

        user_approval = input("Proceed? (y/n) ")
        if user_approval != "y":
            raise CommandError("Exited by user request.")

        # walk through specified directory and compile list of wav files
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                file_path = os.path.join(root, name) 
                print(file_path)

                file_index = int(name.split(".")[0].split("-")[-1])
                print(file_index)

                with open(file_path, 'rb') as file:
                    instance, created = AudioFile.objects.get_or_create(
                        sleep_session=sleep_session,
                        seconds_elapsed=(file_index-1) * audio_length_seconds,
                        defaults={
                            'audio_file': File(
                                file=file, 
                                name=pathlib.Path(file_path).name
                            )
                        }
                    )

        
        

        
        
       





        


        



