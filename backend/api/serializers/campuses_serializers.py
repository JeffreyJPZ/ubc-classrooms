"""
Serializers for buildings resource
"""
from rest_framework import serializers

from .custom_serializer_fields import CampusCodeField, CampusNameField

class CampusSerializer(serializers.Serializer):
    # Serializer for a campus
    campus_code = CampusCodeField(required=True)
    campus_name = CampusNameField(required=True)