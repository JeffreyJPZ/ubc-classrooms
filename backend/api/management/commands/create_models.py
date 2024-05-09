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
    help = "Read timeslot data for a given period from file and create models for tables"

    def handle(self, *args, **options) -> None:
        date = TimetableSettings.START_DATE
        
        # UBCV
        
        # Populate buildings table with new buildings, otherwise do nothing
        for building_code in BuildingCodeToFullName:
            Building.objects.get_or_create(campus=Campus.UBCV.value, building_code=building_code.name, building_name=building_code.value)
                
        # Populate roomtypes table with new roomtypes, otherwise do nothing
        for room in ClassroomType:
            RoomType.objects.get_or_create(campus=Campus.UBCV.value, room_type=room.value)
                
        # Populate timeslots table with unique timeslots, otherwise do nothing
        for building_code in BuildingCodeToFullName:
            path = Path.cwd() / f'{Targets.TIMESLOT_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{date}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{date}_{building_code.name}.csv'

            with open(path, mode="r", newline="") as f:
                reader = csv.DictReader(f, delimiter=",")

                for timeslot in reader:
                    Timeslot.objects.get_or_create(campus=timeslot["Campus"],
                                                    building_code=timeslot["BuildingCode"],
                                                    building_name=timeslot["BuildingName"],
                                                    room=timeslot["Room"],
                                                    room_type=timeslot["RoomType"],
                                                    start=datetime.strptime(timeslot["Start"], TimetableSettings.FORMAT_DATETIME),
                                                    end=datetime.strptime(timeslot["End"], TimetableSettings.FORMAT_DATETIME))
                        
                        

        

