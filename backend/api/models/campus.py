"""
Model for the campus table
"""
from django.db import models

class Campus(models.Model):
    campus_code = models.CharField(primary_key=True, max_length=4, help_text="UBC campus code")
    campus_name = models.CharField(unique=True, null=False, max_length=20, help_text="UBC campus city name")
    