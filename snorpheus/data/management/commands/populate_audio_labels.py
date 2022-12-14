import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from snorpheus.data.models import AudioLabel
from snorpheus.portal.models import Patient, SleepSession


class Command(BaseCommand):
    help = "Reads .csv file containing the class labels for audio data."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", nargs=1, type=str)
        parser.add_argument("patient_id", nargs=1, type=int)
        parser.add_argument("session_id", nargs=1, type=int)

    def handle(self, *args, **options):

        csv_file = options["csv_file"][0]
        filename = csv_file.split("/")[-1].split(".")[0]
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

        audio_files = sleep_session.audio_files.filter(audio_file__contains=filename)

        audio_id = None
        if len(audio_files):
            audio_id = audio_files.first().id

        print(audio_files)
        print("SleepSessionAudio id: ", audio_id)
        print(patient)
        print(sleep_session)

        user_approval = input("Proceed? (y/n) ")
        if user_approval != "y":
            raise CommandError("Exited by user request.")

        audio_events = []

        # opening the CSV file
        with open(csv_file) as file:

            # reading the CSV file
            csvFile = csv.DictReader(file)

            # displaying the contents of the CSV file
            for row in csvFile:
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
            AudioLabel.objects.create(
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
