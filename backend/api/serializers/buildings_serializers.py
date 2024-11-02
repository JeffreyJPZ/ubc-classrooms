"""
Serializers for buildings resource
"""
from rest_framework import serializers

from .custom_serializer_fields import CampusCodeField, BuildingCodeField, BuildingNameField

class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusCodeField(required=True)

class BuildingSerializer(serializers.Serializer):
    # Serializer for a building
    campus = CampusCodeField(required=True)
    building_code = BuildingCodeField(required=True)
    building_name = BuildingNameField(required=True)