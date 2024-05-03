"""
Serializers for roomtypes resource
"""
from rest_framework import serializers

from backend.api.serializers.custom_serializer_fields import *



class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusField()



class RoomTypeSerializer(serializers.Serializer):
    # Serializer for a room type
    room_type = RoomTypeField()