"""
Serializers for roomtypes resource
"""
from rest_framework import serializers

from .custom_serializer_fields import *

class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusField(required=True)

class RoomTypeSerializer(serializers.Serializer):
    # Serializer for a room type
    campus = CampusField(required=True)
    room_type = RoomTypeField(required=True)