"""
Fields for serializers based on UBC infrastructure
"""
from rest_framework import serializers

from utils.ubc import *



# Custom error messages for validation
default_error_messages = {
    "InvalidCampus": "Invalid campus, got {input}",
    "InvalidBuilding": "Invalid building, got {input}",
    "InvalidRoomType": "Invalid room type, got {input}",
}



class CampusField(serializers.Field):
    # Campuses are serialized into campus enums and vice versa
    # E.g. "UBCV" <-> UBCV 

    # Convert campus enum into campus name
    def to_representation(self, value : Campus):
        return value.value
    
    # Convert full name into campus enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == Campus[data].value
        except ValueError:
            raise self.fail("InvalidCampus", input=data)
        
        return Campus[data]
    


class BuildingField(serializers.Field):
    # Buildings are serialized into building enums and vice versa
    # E.g. "Irving K. Barber Learning Centre" <-> IKB 

    # Convert building enum into full name
    def to_representation(self, value : BuildingCodeToFullName):
        return value.value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):

        # Validate
        try:
            assert data == BuildingCodeToFullName[data].value
        except ValueError:
            raise self.fail("InvalidBuilding", input=data)
        
        return BuildingCodeToFullName[data]
        


class RoomTypeField(serializers.Field):
    # Room types are serialized into room type enums and vice versa
    # E.g. "General" <-> GENERAL 

    # Convert building enum into full name
    def to_representation(self, value : ClassroomType):
        return value.value
    
    # Convert full name into building enum
    def to_internal_value(self, data : str):
        
        # Validate
        try:
            assert data == ClassroomType[data].value
        except ValueError:
            raise self.fail("InvalidRoomType", input=data)
        
        return ClassroomType[data]