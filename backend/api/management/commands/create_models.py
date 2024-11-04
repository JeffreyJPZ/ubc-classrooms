"""
Imports the timeslot data into the database
"""
import csv
from pathlib import Path
from django.core.management.base import BaseCommand

from api.utils.targets import *
from api.utils.ubc import *
from api.utils.timetable import *
from api.models.building import *
from api.models.roomtype import *
from api.models.timeslot import *

class Command(BaseCommand):
    help = "Read timeslot data for a given period from file and create models for tables if applicable"

    def handle(self, *args, **options) -> None:
        date = TimetableSettings.START_DATE
        
        # UBCV
        ubcv_campus = Campus.objects.get(pk=CampusEnum.UBCV.name)
                
        # Populate timeslot table with unique timeslots, otherwise do nothing
        for building_code in BuildingCodeToFullName:
            path = Path.cwd() / f'{Targets.TIMESLOT_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{date}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{date}_{building_code.name}.csv'
            building = Building.objects.get(pk=building_code.name)

            with open(path, mode="r", newline="") as f:
                reader = csv.DictReader(f, delimiter=",")

                for timeslot in reader:
                    roomtype = RoomType.objects.get(pk=ClassroomType(timeslot["RoomType"]).value)
                    Timeslot.objects.get_or_create(campus=ubcv_campus,
                                                    building_code=building,
                                                    room=timeslot["Room"],
                                                    room_type=roomtype,
                                                    start=datetime.strptime(timeslot["Start"], TimetableSettings.FORMAT_DATETIME),
                                                    end=datetime.strptime(timeslot["End"], TimetableSettings.FORMAT_DATETIME))
                        
                        

        

