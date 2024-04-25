"""
Model for the timeslot table
"""
from django.db import models

class Timeslot(models.Model):
    campus = models.CharField(max_length=20)
    campus_code = models.CharField(max_length=20)
    building_name = models.CharField(max_length=100)
    building_code = models.CharField(max_length=4)
    room_type = models.CharField(max_length=20)
    room_type_code = models.CharField(max_length=20)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()