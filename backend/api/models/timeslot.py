"""
Model for the timeslot table
"""
from django.db import models

class Timeslot(models.Model):
    campus = models.CharField(max_length=20, help_text="UBC campus code")
    building_code = models.CharField(max_length=4, help_text="3-4 letter code of a UBC building")
    building_name = models.CharField(max_length=100, help_text="Full name of a UBC building")
    room_type = models.CharField(max_length=20, help_text="Whether the room is a general or restricted space")
    start = models.DateTimeField(help_text="Start of the room availability in 'YYYY-MM-DD HH:MM'")
    end = models.DateTimeField(help_text="End of the room availability in 'YYYY-MM-DD HH:MM'")