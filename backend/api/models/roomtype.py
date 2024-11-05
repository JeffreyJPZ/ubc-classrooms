"""
Model for the roomtype table
"""
from django.db import models
from .campus import Campus

class RoomType(models.Model):
    campus = models.ForeignKey(to=Campus, db_column="campus", to_field="campus_code", on_delete=models.CASCADE, null=False, max_length=4, help_text="Foreign key for UBC campus")
    room_type = models.CharField(primary_key=True, max_length=20, help_text="Whether the room is a general or restricted space")