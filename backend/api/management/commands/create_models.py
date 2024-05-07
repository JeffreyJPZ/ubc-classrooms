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
        # TODO: replace hardcoded date and buildings for prod
        date = "2024-03-25"
        buildings = [BuildingCodeToFullName["ALRD"], BuildingCodeToFullName["SWNG"]]

        # Populate buildings table with new buildings, otherwise do nothing
        for building_code in BuildingCodeToFullName:
            Building.objects.get_or_create(building_code=building_code.name, building_name=building_code.value)
                
        # Populate roomtypes table with new roomtypes, otherwise do nothing
        for room in ClassroomType:
            RoomType.objects.get_or_create(room_type=room.value)
                
        # Populate timeslots table with unique timeslots, otherwise do nothing
        for building_code in buildings:
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
                        
                        

        

