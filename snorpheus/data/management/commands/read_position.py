import datetime

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Reads .txt file containing position data."

    def add_arguments(self, parser):
        parser.add_argument("txt_file", nargs=1, type=str)

    def handle(self, *args, **options):

        txt_file = options["txt_file"][0]

        position_events = []

        with open(txt_file) as file:
            for line in file:
                split_line = line.split("->")
                timestamp = split_line[0]
                coords = split_line[1].split()
                print(timestamp)
                position_events.push(
                    {
                        "timestamp": datetime.datetime(2021, 8, 22, 11, 2, 5),
                        "x": coords[0],
                        "y": coords[1],
                        "z": coords[2],
                    }
                )
