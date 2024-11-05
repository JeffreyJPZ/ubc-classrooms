"""
Serializers for timeslots resource
"""
from rest_framework import serializers

from .custom_serializer_fields import CampusCodeField, BuildingCodeField, BuildingNameField, RoomTypeField
    
class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusCodeField(required=True)

class QueryParametersSerializer(serializers.Serializer):
    # Serializer for validating query parameters
    date = serializers.DateField(format="%Y-%m-%d", required=True)
    start = serializers.TimeField(format="%H:%M", allow_null=True)
    end = serializers.TimeField(format="%H:%M", allow_null=True)
    buildings = serializers.ListField(child=BuildingCodeField(), allow_empty=True)
    room_types = serializers.ListField(child=RoomTypeField(), allow_empty=True)

class TimeslotSerializer(serializers.Serializer):
    # Serializer for a timeslot
    campus = CampusCodeField(required=True)
    building_code = BuildingCodeField(required=True)
    building_name = BuildingNameField(required=True)
    room = serializers.CharField(required=True)
    room_type = RoomTypeField(required=True)
    date = serializers.DateField(format="%Y-%m-%d", required=True)
    start = serializers.TimeField(format="%H:%M", required=True)
    end = serializers.TimeField(format="%H:%M", required=True)
