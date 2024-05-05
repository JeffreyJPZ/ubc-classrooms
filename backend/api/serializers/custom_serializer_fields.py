"""
Fields for serializers based on UBC infrastructure
"""
from rest_framework import serializers

from utils.ubc import *

# Custom error messages for validation
default_error_messages = {
    "InvalidCampus": "Invalid campus, got {input}",
    "InvalidBuildingCode": "Invalid building code, got {input}",
    "InvalidBuildingName": "Invalid building name, got {input}",
    "InvalidRoomType": "Invalid room type, got {input}",
}

class CampusField(serializers.Field):
    # Campuses are verified
    # e.g. "UBCV" <-> "UBCV"

    # Convert campus enum into campus name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into campus enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == Campus[data].value
        except ValueError:
            raise self.fail("InvalidCampus", input=data)
        
        return data
    


class BuildingCodeField(serializers.Field):
    # Building codes are verified
    # e.g. "IKB" <-> "IKB"

    # Convert building enum into full name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName[data].name
        except ValueError:
            raise self.fail("InvalidBuildingCode", input=data)
        
        return data
    


class BuildingNameField(serializers.Field):
    # Building names are verified
    # e.g. "Irving K. Barber Learning Centre" <-> "Irving K. Barber Learning Centre"

    # Convert building enum into full name
    def to_representation(self, value : str):
        return value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName[data].value
        except ValueError:
            raise self.fail("InvalidBuildingName", input=data)
        
        return data
        


class RoomTypeField(serializers.Field):
    # Room types are verified
    # e.g. "General" <-> "General"

    # Convert building enum into full name
    def to_representation(self, value : str):
        return value.value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):
        
        # Validate
        try:
            assert data == ClassroomType[data].value
        except ValueError:
            raise self.fail("InvalidRoomType", input=data)
        
        return data