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

    def handle(self) -> None:
        date = TimetableSettings.START_DATE
        
        # Populate campus table with new campuses, otherwise do nothing
        for campus in CampusEnum:
            Campus.objects.get_or_create(campus_code=campus.name, campus_name=campus.value)

        # UBCV
        ubcv_campus = Campus.objects.get(pk=CampusEnum.UBCV.name)

        # Populate building table with new buildings, otherwise do nothing
        for building_code in BuildingCodeToFullName:
            Building.objects.get_or_create(campus=ubcv_campus, building_code=building_code.name, building_name=building_code.value)
                
        # Populate roomtype table with new roomtypes, otherwise do nothing
        for room in ClassroomType:
            RoomType.objects.get_or_create(campus=ubcv_campus, room_type=room.value)
                
        # Populate timeslot table with unique timeslots, otherwise do nothing
        for building_code in BuildingCodeToFullName:
            path = Path.cwd() / f'{Targets.TIMESLOT_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{date}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{date}_{building_code.name}.csv'
            building = Building.objects.get(pk=building_code.name)

            with open(path, mode="r", newline="") as f:
                reader = csv.DictReader(f, delimiter=",")

                for timeslot in reader:
                    roomtype = RoomType.objects.get(pk=ClassroomType(timeslot["RoomType"]).value)
                    Timeslot.objects.get_or_create(campus=ubcv_campus,
                                                    building=building,
                                                    room=timeslot["Room"],
                                                    room_type=roomtype,
                                                    start=datetime.strptime(timeslot["Start"], TimetableSettings.FORMAT_DATETIME),
                                                    end=datetime.strptime(timeslot["End"], TimetableSettings.FORMAT_DATETIME))
                        
                        

        

