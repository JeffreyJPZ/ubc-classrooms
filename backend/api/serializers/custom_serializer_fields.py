"""
Fields for serializers based on UBC infrastructure
"""
from rest_framework import serializers

from api.utils.ubc import *

class CampusField(serializers.CharField):
    # Campuses are verified
    # e.g. "UBCV" <-> "UBCV"
    
    # Custom error messages for validation
    default_error_messages = {
        "InvalidCampus": "Invalid campus, got {input}",
    }

    # Convert campus enum into campus name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into campus enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == Campus[data].value
        except KeyError:
            raise self.fail("InvalidCampus", input=data)
        
        return data
    


class BuildingCodeField(serializers.CharField):
    # Building codes are verified
    # e.g. "IKB" <-> "IKB"

    default_error_messages = {
        "InvalidBuildingCode": "Invalid building code, got {input}",
    }

    # Convert building enum into full name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName[data].name
        except KeyError:
            raise self.fail("InvalidBuildingCode", input=data)
        
        return data
    


class BuildingNameField(serializers.CharField):
    # Building names are verified
    # e.g. "Irving K. Barber Learning Centre" <-> "Irving K. Barber Learning Centre"

    default_error_messages = {
        "InvalidBuildingName": "Invalid building name, got {input}",
    }

    # Convert building enum into full name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName(data).value
        except ValueError:
            raise self.fail("InvalidBuildingName", input=data)
        
        return data
        


class RoomTypeField(serializers.CharField):
    # Room types are verified
    # e.g. "General" <-> "General"

    default_error_messages = {
        "InvalidRoomType": "Invalid room type, got {input}",
    }

    # Convert building enum into full name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):
        
        # Validate
        try:
            assert data == ClassroomType(data).value
        except ValueError:
            raise self.fail("InvalidRoomType", input=data)
        
        return data