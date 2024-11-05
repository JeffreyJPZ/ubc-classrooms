"""
Serializers for roomtypes resource
"""
from rest_framework import serializers

from .custom_serializer_fields import CampusCodeField, RoomTypeField

class PathParametersSerializer(serializers.Serializer):
    # Serializer for validating path parameters
    campus = CampusCodeField(required=True)

class RoomTypeSerializer(serializers.Serializer):
    # Serializer for a room type
    campus = CampusCodeField(required=True)
    room_type = RoomTypeField(required=True)