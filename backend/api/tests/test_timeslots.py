"""
API tests for timeslots resource
"""
from rest_framework.test import APITestCase
from datetime import datetime

from api.models.timeslot import *

# Version 1

class TestTimeslotsV1(APITestCase):
    def createTimeslots():
        Timeslot.objects.create(campus="UBCV", building_code="ALRD", building_name="Allard Hall", room=105, room_type="General", start=datetime.strptime("2024-05-03 15:00", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-03 18:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.create(campus="UBCV", building_code="SWNG", building_name="West Mall Swing Space", room=200, room_type="Restricted", start=datetime.strptime("2024-05-03 16:00", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-03 17:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.create(campus="UBCV", building_code="LIFE", building_name="UBC Life Building", room=2201, room_type="General", start=datetime.strptime("2024-05-03 08:00", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-03 11:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.create(campus="UBCV", building_code="ESB", building_name="Earth Sciences Building", room=1013, room_type="General", start=datetime.strptime("2024-05-04 12:30", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-04 14:30", "%Y-%m-%d %H:%M"))

    def testGetMatchingDateStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03")
        self.assertEqual(response.status_code, 200)

    def testGetMatchingDateAndTimeStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04&start=12:30&end=14:30")
        self.assertEqual(response.status_code, 200)

    def testGetMatchingRoomTypeStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&room_types=Restricted")
        self.assertEqual(response.status_code, 200)

    def testGetMatchingBuildingStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04&buildings=ESB")
        self.assertEqual(response.status_code, 200)

    def testGetMatchingMultipleParamsStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&start=16:00&end=17:00&room_types=General&room_types=Restricted&buildings=ALRD&buildings=LIFE&buildings=SWNG")
        self.assertEqual(response.status_code, 200)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03")
        self.assertEqual(response.status_code, 200)

    def testGetNoMatchingBuildingStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&buildings=ICCS&buildings=LSK")
        self.assertEqual(response.status_code, 200)
    
    def testGetNoMatchingRoomTypeStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04&room_types=Restricted")
        self.assertEqual(response.status_code, 200)
    
    def testGetNoMatchingDateStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-05")
        self.assertEqual(response.status_code, 200)

    def testGetNoMatchingDateAndTimeStatusOk(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&start=14:30&end=16:30")
        self.assertEqual(response.status_code, 200)

    def testGetMalformedParametersStatusBadRequest(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="dat=2024-05-03&begin=14:00&stop=15:00&building=ICCS&room_type=General")
        self.assertEqual(response.status_code, 400)

    def testGetMalformedValueStatusBadRequest(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=xyz&start=aaa&end=123456&buildings=yes&room_types=no")
        self.assertEqual(response.status_code, 400)

    def testGetStatusNotFound(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.get('/api/v1/timeslots/UBCO/', QUERY_STRING="date=2024-05-03")
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        TestTimeslotsV1.createTimeslots()
        response = self.client.post('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04")
        self.assertEqual(response.status_code, 405)