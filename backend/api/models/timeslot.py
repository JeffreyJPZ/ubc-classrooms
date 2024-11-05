"""
Model for the timeslot table
"""
from django.db import models
from .campus import Campus
from .building import Building
from .roomtype import RoomType

class Timeslot(models.Model):
    campus = models.ForeignKey(to=Campus, db_column="campus", to_field="campus_code", on_delete=models.CASCADE, null=False, max_length=4, help_text="Foreign key for UBC campus")
    building_code = models.ForeignKey(to=Building, db_column="building_code", to_field="building_code", on_delete=models.CASCADE, null=False, max_length=4, help_text="Foreign key for UBC building")
    room = models.CharField(help_text="Room number associated with the availability")
    room_type = models.ForeignKey(to=RoomType, db_column="room_type", to_field="room_type", on_delete=models.CASCADE, null=False, max_length=20, help_text="Foreign key for UBC room type")
    start = models.DateTimeField(help_text="Start of the room availability in 'YYYY-MM-DD HH:MM'")
    end = models.DateTimeField(help_text="End of the room availability in 'YYYY-MM-DD HH:MM'")