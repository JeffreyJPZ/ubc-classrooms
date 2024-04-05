"""
Serializers for validating parameters and returning timeslots
"""
from rest_framework import serializers

from utils.ubc import *
from custom_fields import *
    


class PathParametersSerializer(serializers.Serializer):
    # Validate path parameters
    campus = CampusField()



class QueryParametersSerializer(serializers.Serializer):
    # Validate query parameters
    
    date = serializers.DateField(format="iso-8601", required=True)
    start = serializers.TimeField(format="%H:%M", required=False)
    end = serializers.TimeField(format="%H:%M", required=False)
    buildings = serializers.ListField(child=BuildingField(), allow_empty=True)
    roomtypes = serializers.ListField(child=RoomTypeField(), allow_empty=True)



class TimeslotsSerializer(serializers.Serializer):
    # Serializes timeslots fields for output 

    campus = CampusField()
    building = BuildingField()
    roomtype = RoomTypeField()
    date = serializers.DateField(format="iso-8601", required=True)
    start = serializers.TimeField(format="%H:%M", required=False)
    end = serializers.TimeField(format="%H:%M", required=False)
