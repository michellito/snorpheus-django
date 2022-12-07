import csv
import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from snorpheus.data.models import AudioLabel
from snorpheus.portal.models import Patient, SleepSession


class Command(BaseCommand):
    help = "Reads .csv file containing the class labels for audio data."

    def add_arguments(self, parser):
        parser.add_argument("directory", nargs=1, type=str)
        parser.add_argument("patient_id", nargs=1, type=int)
        parser.add_argument("session_id", nargs=1, type=int)

    def handle(self, *args, **options):

        directory = options["directory"][0]
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
        
        user_approval = input("Proceed? (y/n) ")
        if user_approval != "y":
            raise CommandError("Exited by user request.")


        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:

                file_name = name.split(".")[0]
                file_path = os.path.join(root, name) 
                print(file_path)

                audio_files = sleep_session.audio_files.filter(audio_file__contains=file_name)

                audio_id = None
                if len(audio_files):
                    audio_id = audio_files.first().id
                
                audio_events = []

                # opening the CSV file
                with open(file_path) as file:

                    # reading the CSV file
                    csv_dict = csv.DictReader(file)

                    # displaying the contents of the CSV file
                    for row in csv_dict:
                        audio_events.append(
                            {
                                "seconds_elapsed": row["timestamp"],
                                "label_1": row["class1"],
                                "label_2": row["class2"],
                                "label_3": row["class3"],
                                "score_1": row["score1"],
                                "score_2": row["score2"],
                                "score_3": row["score3"],
                            }
                        )

                    print(audio_events[0])

                print("File was read successfully, creating AudioLabel objects...")

                created_count = 0

                for event in audio_events:
                    instance, created = AudioLabel.objects.get_or_create(
                        audio_file_id=audio_id,
                        seconds_elapsed=event["seconds_elapsed"],
                        label_1=event["label_1"],
                        label_2=event["label_2"],
                        label_3=event["label_3"],
                        score_1=event["score_1"],
                        score_2=event["score_2"],
                        score_3=event["score_3"],
                    )
                    created_count += 1

                print("%s AudioLabel objects created" % str(created_count))
