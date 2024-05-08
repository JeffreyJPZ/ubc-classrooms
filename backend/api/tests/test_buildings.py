"""
API tests for buildings resource
"""
from rest_framework.test import APITestCase

from api.models.building import *

# Version 1

class TestBuildingsV1(APITestCase):
    def createBuildings():
        Building.objects.create(campus="UBCV", building_code="ALRD", building_name="Allard Hall")
        Building.objects.create(campus="UBCV", building_code="SWNG", building_name="West Mall Swing Space")

    def testGetStatusOk(self):
        TestBuildingsV1.createBuildings()
        response = self.client.get('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetStatusNotFound(self):
        TestBuildingsV1.createBuildings()
        response = self.client.get('/api/v1/buildings/UBCO/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        TestBuildingsV1.createBuildings()
        response = self.client.post('/api/v1/buildings/UBCV/')
        self.assertEqual(response.status_code, 405)