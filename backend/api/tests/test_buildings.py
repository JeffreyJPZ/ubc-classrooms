"""
API tests for buildings resource
"""
from rest_framework.test import APITestCase

from api.models.campus import *
from api.models.building import *

# Version 1

class TestBuildingsV1(APITestCase):
    def setUp(self):
        ubcv_campus = Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")[0]
        Building.objects.get_or_create(campus=ubcv_campus, building_code="ALRD", building_name="Allard Hall", building_address="1822 East Mall", latitude=49.2699, longitude=-123.25318)
        Building.objects.get_or_create(campus=ubcv_campus, building_code="SWNG", building_name="West Mall Swing Space", building_address="2175 West Mall", latitude=49.26293, longitude=-123.25431)

    def testGetStatusOk(self):
        response = self.client.get('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/buildings/UBCO/')
        self.assertEqual(response.status_code, 200)

    def testGetStatusNotFound(self):
        response = self.client.get('/api/v1/buildings/UBCA/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 405)



class TestBuildingsV2(APITestCase):
    def setUp(self):
        ubcv_campus = Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")[0]
        Building.objects.get_or_create(campus=ubcv_campus, building_code="ALRD", building_name="Allard Hall", building_address="1822 East Mall", latitude=49.2699, longitude=-123.25318)
        Building.objects.get_or_create(campus=ubcv_campus, building_code="SWNG", building_name="West Mall Swing Space", building_address="2175 West Mall", latitude=49.26293, longitude=-123.25431)

    def testGetStatusOk(self):
        response = self.client.get('/api/v2/buildings/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v2/buildings/UBCO/')
        self.assertEqual(response.status_code, 200)

    def testGetStatusNotFound(self):
        response = self.client.get('/api/v2/buildings/UBCA/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v2/buildings/UBCV/')
        self.assertEqual(response.status_code, 405)