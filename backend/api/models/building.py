"""
Model for the building table
"""
from django.db import models
from .campus import Campus

class Building(models.Model):
    campus = models.ForeignKey(to=Campus, db_column="campus", to_field="campus_code", on_delete=models.CASCADE, null=False, max_length=4, help_text="Foreign key for UBC campus")
    building_code = models.CharField(primary_key=True, max_length=4, help_text="3-4 letter code of a UBC building")
    building_name = models.CharField(unique=True, null=False, max_length=100, help_text="Full name of a UBC building")
    building_address = models.CharField(null=False, default="", db_default="", max_length=100, help_text="Street address of a UBC building")
    latitude = models.DecimalField(null=False, default=0, db_default=0, max_digits=8, decimal_places=6, help_text="Latitude data of a UBC building up to 5 significant figures")
    longitude = models.DecimalField(null=False, default=0, db_default=0, max_digits=9, decimal_places=6, help_text="Longitude data of a UBC building up to 5 significant figures")
    