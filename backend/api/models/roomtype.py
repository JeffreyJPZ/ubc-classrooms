"""
Model for the roomtype table
"""
from django.db import models

class RoomType(models.Model):
    campus = models.CharField(max_length=4, help_text="UBC campus code")
    room_type = models.CharField(max_length=20, help_text="Whether the room is a general or restricted space")