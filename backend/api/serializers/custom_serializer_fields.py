"""
Fields for serializers based on UBC infrastructure
"""
from rest_framework import serializers

from api.utils.ubc import *

class CampusCodeField(serializers.CharField):
    # Campus codes are verified
    # Used for Campus, Building, RoomType, Timeslot serializers
    # e.g. "UBCV" <-> "UBCV"
    
    default_error_messages = {
        "InvalidCampusCode": "Invalid campus code, got {input}",
    }

    def to_representation(self, value : str):
        return value
    
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == CampusEnum[data].name
        except KeyError:
            raise self.fail("InvalidCampusCode", input=data)
        
        return data



class CampusNameField(serializers.CharField):
    # Campus names are verified
    # Used for Campus serializer
    # e.g. "Vancouver" <-> "Vancouver"
    
    default_error_messages = {
        "InvalidCampusName": "Invalid campus name, got {input}",
    }

    def to_representation(self, value : str):
        return value
    
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == CampusEnum(data).value
        except KeyError:
            raise self.fail("InvalidCampusName", input=data)
        
        return data
    


class BuildingCodeField(serializers.CharField):
    # Building codes are verified
    # Used for Building, Timeslot serializer
    # e.g. "IKB" <-> "IKB"

    default_error_messages = {
        "InvalidBuildingCode": "Invalid building code, got {input}",
    }

    def to_representation(self, value : str):
        return value
    
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName[data].name
        except KeyError:
            raise self.fail("InvalidBuildingCode", input=data)
        
        return data
    


class BuildingNameField(serializers.CharField):
    # Building names are verified
    # Used for Building serializer
    # e.g. "Irving K. Barber Learning Centre" <-> "Irving K. Barber Learning Centre"

    default_error_messages = {
        "InvalidBuildingName": "Invalid building name, got {input}",
    }

    def to_representation(self, value : str):
        return value
    
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName(data).value
        except ValueError:
            raise self.fail("InvalidBuildingName", input=data)
        
        return data
        


class RoomTypeField(serializers.CharField):
    # Room types are verified
    # Used for RoomType, Timeslot serializer
    # e.g. "General" <-> "General"

    default_error_messages = {
        "InvalidRoomType": "Invalid room type, got {input}",
    }

    def to_representation(self, value : str):
        return value
    
    def to_internal_value(self, data : str):
        
        # Validate
        try:
            assert data == ClassroomType(data).value
        except ValueError:
            raise self.fail("InvalidRoomType", input=data)
        
        return data