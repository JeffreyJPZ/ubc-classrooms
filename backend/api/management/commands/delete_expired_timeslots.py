"""
Clear expired timeslots
"""
from django.core.management.base import BaseCommand

from api.utils.targets import *
from api.utils.ubc import *
from api.utils.timetable import *
from api.models.building import *
from api.models.roomtype import *
from api.models.timeslot import *

class Command(BaseCommand):
    help = "Delete timeslots older than a given date"

    def handle(self, *args, **options) -> None:
        date = TimetableSettings.START_DATE

        # Delete expired timeslots
        Timeslot.objects.filter(start__lt=datetime.strptime(date + " 00:00", TimetableSettings.FORMAT_DATETIME)).delete()