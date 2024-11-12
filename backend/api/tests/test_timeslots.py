"""
API tests for timeslots resource
"""
from rest_framework.test import APITestCase
from datetime import datetime

from .utils import BytestoString
from api.models.campus import *
from api.models.building import *
from api.models.roomtype import *
from api.models.timeslot import *

# Version 1
class TimeslotsResponseV1:
    __alrd__ = {"campus": "UBCV", "building_code": "ALRD", "building_name": "Allard Hall", "room": "105", "room_type": "General", "date": "2024-05-03", "start": "15:00", "end": "18:00"}
    __swng__ = {"campus": "UBCV", "building_code": "SWNG", "building_name": "West Mall Swing Space", "room": "200", "room_type": "Restricted", "date": "2024-05-03", "start": "16:00", "end": "17:00"}
    __life__ = {"campus": "UBCV", "building_code": "LIFE", "building_name": "UBC Life Building", "room": "B101", "room_type": "General", "date": "2024-05-03", "start": "08:00", "end": "11:00"}
    __esb__ = {"campus": "UBCV", "building_code": "ESB", "building_name": "Earth Sciences Building", "room": "1013", "room_type": "General", "date": "2024-05-04", "start": "12:30", "end": "14:30"}

    ubcv_response_data_matching_date = [__alrd__, __swng__, __life__]
    ubcv_response_data_matching_date_and_time = [__esb__]
    ubcv_response_data_matching_room_type = [__swng__]
    ubcv_response_data_matching_building = [__esb__]
    ubcv_response_data_matching_multiple_params = [__alrd__, __swng__]
    ubcv_response_data_no_matches = []

    ubco_response_data = []

class TestTimeslotsV1(APITestCase):
    def setUp(self):
        ubcv_campus = Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")[0]
        alrd = Building.objects.get_or_create(campus=ubcv_campus, building_code="ALRD", building_name="Allard Hall", building_address="1822 East Mall", latitude=49.2699, longitude=-123.25318)[0]
        swng = Building.objects.get_or_create(campus=ubcv_campus, building_code="SWNG", building_name="West Mall Swing Space", building_address="2175 West Mall", latitude=49.26293, longitude=-123.25431)[0]
        life = Building.objects.get_or_create(campus=ubcv_campus, building_code="LIFE", building_name="UBC Life Building", building_address="6138 Student Union Blvd", latitude=49.26765, longitude=-123.25006)[0]
        esb = Building.objects.get_or_create(campus=ubcv_campus, building_code="ESB", building_name="Earth Sciences Building", building_address="2207 Main Mall", latitude=49.26274, longitude=-123.25224)[0]
        general = RoomType.objects.get_or_create(campus=ubcv_campus, room_type="General")[0]
        restricted = RoomType.objects.get_or_create(campus=ubcv_campus, room_type="Restricted")[0]

        Timeslot.objects.get_or_create(campus=ubcv_campus, building_code=alrd, room="105", room_type=general, start=datetime.strptime("2024-05-03 15:00", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-03 18:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.get_or_create(campus=ubcv_campus, building_code=swng, room="200", room_type=restricted, start=datetime.strptime("2024-05-03 16:00", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-03 17:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.get_or_create(campus=ubcv_campus, building_code=life, room="B101", room_type=general, start=datetime.strptime("2024-05-03 08:00", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-03 11:00", "%Y-%m-%d %H:%M"))
        Timeslot.objects.get_or_create(campus=ubcv_campus, building_code=esb, room="1013", room_type=general, start=datetime.strptime("2024-05-04 12:30", "%Y-%m-%d %H:%M"), end=datetime.strptime("2024-05-04 14:30", "%Y-%m-%d %H:%M"))

    def testGetMatchingDateStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_matching_date)

    def testGetMatchingDateAndTimeStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04&start=12:30&end=14:30")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_matching_date_and_time)

    def testGetMatchingRoomTypeStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&room_types=Restricted")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_matching_room_type)

    def testGetMatchingBuildingStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04&buildings=ESB")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_matching_building)

    def testGetMatchingMultipleParamsStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&start=16:00&end=17:00&room_types=General&room_types=Restricted&buildings=ALRD&buildings=LIFE&buildings=SWNG")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_matching_multiple_params)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCO/', QUERY_STRING="date=2024-05-03")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubco_response_data)

    def testGetNoMatchingBuildingStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&buildings=ICCS&buildings=LSK")
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_no_matches)
    
    def testGetNoMatchingRoomTypeStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04&room_types=Restricted")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_no_matches)
    
    def testGetNoMatchingDateStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-05")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_no_matches)

    def testGetNoMatchingDateAndTimeStatusOk(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-03&start=14:30&end=16:30")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), TimeslotsResponseV1.ubcv_response_data_no_matches)

    def testGetMalformedParametersStatusBadRequest(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="dat=2024-05-03&begin=14:00&stop=15:00&building=ICCS&room_type=General")
        self.assertEqual(response.status_code, 400)

    def testGetMalformedValueStatusBadRequest(self):
        response = self.client.get('/api/v1/timeslots/UBCV/', QUERY_STRING="date=xyz&start=aaa&end=123456&buildings=yes&room_types=no")
        self.assertEqual(response.status_code, 400)

    def testGetStatusNotFound(self):
        response = self.client.get('/api/v1/timeslots/UBCA/', QUERY_STRING="date=2024-05-03")
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v1/timeslots/UBCV/', QUERY_STRING="date=2024-05-04")
        self.assertEqual(response.status_code, 405)