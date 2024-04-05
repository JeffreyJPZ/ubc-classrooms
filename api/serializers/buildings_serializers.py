"""
Serializers for validating parameters and returning buildings
"""
from rest_framework import serializers

from custom_fields import *



class PathParametersSerializer(serializers.Serializer):
    # Validate path parameters
    campus = CampusField()