"""
Serializers for timeslots resource
"""
from rest_framework import serializers

from utils.ubc import *
from backend.api.serializers.custom_serializer_fields import *
    


class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusField()



class QueryParametersSerializer(serializers.Serializer):
    # Serializer for validating query parameters
    date = serializers.DateField(format="iso-8601", required=True)
    start = serializers.TimeField(format="%H:%M", required=False)
    end = serializers.TimeField(format="%H:%M", required=False)
    buildings = serializers.ListField(child=BuildingCodeField(), allow_empty=True)
    room_types = serializers.ListField(child=RoomTypeField(), allow_empty=True)



class TimeslotSerializer(serializers.Serializer):
    # Serializer for a timeslot
    campus = CampusField()
    building_code = BuildingCodeField()
    building_name = BuildingNameField()
    room_type = RoomTypeField()
    date = serializers.DateField(format="iso-8601", required=True)
    start = serializers.TimeField(format="%H:%M", required=False)
    end = serializers.TimeField(format="%H:%M", required=False)
