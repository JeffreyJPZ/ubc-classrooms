"""
Serializers for buildings resource
"""
from rest_framework import serializers

from .custom_serializer_fields import CampusCodeField, BuildingCodeField, BuildingNameField

class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusCodeField(required=True)

# Version 1

class BuildingSerializerV1(serializers.Serializer):
    # Serializer for a building
    campus = CampusCodeField(required=True)
    building_code = BuildingCodeField(required=True)
    building_name = BuildingNameField(required=True)

# Version 2

class BuildingSerializerV2(serializers.Serializer):
    # Serializer for a building
    campus = CampusCodeField(required=True)
    building_code = BuildingCodeField(required=True)
    building_name = BuildingNameField(required=True)
    building_address = serializers.CharField(required=True, allow_blank=True)
    latitude = serializers.DecimalField(max_digits=8, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)