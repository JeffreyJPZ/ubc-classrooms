"""
API tests for buildings resource
"""
from rest_framework.test import APITestCase

from .utils import BytestoString
from api.models.campus import *
from api.models.building import *

# Version 1

class BuildingsResponseV1:
    ubcv_response_data = [
        {"campus": "UBCV", "building_code": "ALRD", "building_name": "Allard Hall"},
        {"campus": "UBCV", "building_code": "SWNG", "building_name": "West Mall Swing Space"}
    ]
    ubco_response_data = []

class TestBuildingsV1(APITestCase):
    def setUp(self):
        ubcv_campus = Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")[0]
        Building.objects.get_or_create(campus=ubcv_campus, building_code="ALRD", building_name="Allard Hall", building_address="1822 East Mall", latitude=49.269900, longitude=-123.253180)
        Building.objects.get_or_create(campus=ubcv_campus, building_code="SWNG", building_name="West Mall Swing Space", building_address="2175 West Mall", latitude=49.262930, longitude=-123.254310)

    def testGetStatusOk(self):
        response = self.client.get('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), BuildingsResponseV1.ubcv_response_data)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/buildings/UBCO/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), BuildingsResponseV1.ubco_response_data)

    def testGetStatusNotFound(self):
        response = self.client.get('/api/v1/buildings/UBCA/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 405)

# Version 2

class BuildingsResponseV2:
    ubcv_response_data = [
        {"campus": "UBCV", "building_code": "ALRD", "building_name": "Allard Hall", "building_address": "1822 East Mall", "latitude":"49.269900", "longitude": "-123.253180"},
        {"campus": "UBCV", "building_code": "SWNG", "building_name": "West Mall Swing Space", "building_address": "2175 West Mall", "latitude": "49.262930", "longitude": "-123.254310"}
    ]
    ubco_response_data = []

class TestBuildingsV2(APITestCase):
    def setUp(self):
        ubcv_campus = Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")[0]
        Building.objects.get_or_create(campus=ubcv_campus, building_code="ALRD", building_name="Allard Hall", building_address="1822 East Mall", latitude=49.269900, longitude=-123.253180)
        Building.objects.get_or_create(campus=ubcv_campus, building_code="SWNG", building_name="West Mall Swing Space", building_address="2175 West Mall", latitude=49.262930, longitude=-123.254310)

    def testGetStatusOk(self):
        response = self.client.get('/api/v2/buildings/UBCV/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), BuildingsResponseV2.ubcv_response_data)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v2/buildings/UBCO/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), BuildingsResponseV2.ubco_response_data)

    def testGetStatusNotFound(self):
        response = self.client.get('/api/v2/buildings/UBCA/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v2/buildings/UBCV/')
        self.assertEqual(response.status_code, 405)