"""
API tests for timeslots resource
"""
from rest_framework import status
from rest_framework.test import APITestCase

from datetime import datetime
from models.timeslot import *

class TestTimeslotsV1(APITestCase):
    def createTimeslots():
        Timeslot.objects.create(campus="UBCV", building_code="ALRD", building_name="Allard Hall", room=105, roomtype="General", start=datetime.strftime("2024-05-03 15:00", "%Y-%m-%d %H:%M"), end=datetime.strftime("2024-05-03 18:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.create(campus="UBCV", building_code="SWNG", building_name="West Mall Swing Space", room=200, roomtype="Restricted", start=datetime.strftime("2024-05-03 16:00", "%Y-%m-%d %H:%M"), end=datetime.strftime("2024-05-03 17:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.create(campus="UBCV", building_code="LIFE", building_name="UBC Life Building", room=2201, roomtype="General", start=datetime.strftime("2024-05-03 08:00", "%Y-%m-%d %H:%M"), end=datetime.strftime("2024-05-03 11:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.create(campus="UBCV", building_code="ESB", building_name="Earth Sciences Building", room=1013, roomtype="General", start=datetime.strftime("2024-05-04 12:30", "%Y-%m-%d %H:%M"), end=datetime.strftime("2024-05-04 14:30", "%Y-%m-%d %H:%M"))

    def getMatchingDateStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-03")
        self.assertTrue(status.is_success(response.status_code))

    def getWMatchingDateAndTimeStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-04&start=12:30&end=14:30")
        self.assertTrue(status.is_success(response.status_code))

    def getMatchingRoomTypeStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-03&room_types=Restricted")
        self.assertTrue(status.is_success(response.status_code))

    def getMatchingBuildingStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-04&buildings=ESB")
        self.assertTrue(status.is_success(response.status_code))

    def getMatchingMultipleParamsStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-03&start=16:00&end=17:00&room_types=General&room_types=Restricted&buildings=ALRD&buildings=LIFE&buildings=SWNG")
        self.assertTrue(status.is_success(response.status_code))

    def getEmptyDBStatusNotFound(self):
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-03")
        self.assertTrue(status.is_client_error(response.status_code))

    def getNoMatchingBuildingStatusNotFound(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-03&buildings=ICCS&buildings=LSK")
        self.assertTrue(status.is_client_error(response.status_code))
    
    def getNoMatchingRoomTypeStatusNotFound(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-04&room_types=Restricted")
        self.assertTrue(status.is_client_error(response.status_code))
    
    def getNoMatchingDateStatusNotFound(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-05")
        self.assertTrue(status.is_client_error(response.status_code))

    def getNoMatchingDateAndTimeStatusNotFound(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCV', QUERY_STRING="date=2024-05-03&start=14:00&end=17:00")
        self.assertTrue(status.is_client_error(response.status_code))

    def getStatusBadRequest(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('timeslots/UBCO', QUERY_STRING="date=2024-05-03")
        self.assertTrue(status.is_client_error(response.status_code))

    def postStatusMethodNotAllowed(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.post('timeslots/UBCV', QUERY_STRING="date=2024-05-04")
        self.assertTrue(status.is_client_error(response.status_code))