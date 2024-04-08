"""
Serializers for buildings resource
"""
from rest_framework import serializers

from custom_fields import *



class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusField()



class BuildingSerializer(serializers.Serializer):
    # Serializer for a building
    building_code = BuildingCodeField()
    building_name = BuildingNameField()