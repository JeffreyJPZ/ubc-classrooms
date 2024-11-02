"""
Model for the building table
"""
from django.db import models
from .campus import Campus

class Building(models.Model):
    campus = models.ForeignKey(to=Campus, db_column="campus", to_field="campus_code", on_delete=models.CASCADE, null=False, max_length=4, help_text="Foreign key for UBC campus")
    building_code = models.CharField(primary_key=True, max_length=4, help_text="3-4 letter code of a UBC building")
    building_name = models.CharField(unique=True, null=False, max_length=100, help_text="Full name of a UBC building")
    