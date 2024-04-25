"""
Model for the building table
"""
from django.db import models

class Building(models.Model):
    campus = models.CharField(max_length=20)
    campus_code = models.CharField(max_length=20)
    building_name = models.CharField(max_length=100)
    building_code = models.CharField(max_length=4)