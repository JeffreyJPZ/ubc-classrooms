"""
Model for the roomtype table
"""
from django.db import models

class RoomType(models.Model):
    campus = models.CharField(max_length=20)
    campus_code = models.CharField(max_length=20)
    building_name = models.CharField(max_length=100)
    building_code = models.CharField(max_length=4)
    room_type = models.CharField(max_length=20)
    room_type_code = models.CharField(max_length=20)