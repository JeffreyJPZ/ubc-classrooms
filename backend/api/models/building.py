"""
Model for the building table
"""
from django.db import models

class Building(models.Model):
    building_code = models.CharField(max_length=4, help_text="3-4 letter code of a UBC building")
    building_name = models.CharField(max_length=100, help_text="Full name of a UBC building")