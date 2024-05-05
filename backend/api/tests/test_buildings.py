"""
API tests for buildings resource
"""
from rest_framework import status
from rest_framework.test import APITestCase

from models.building import *

class TestBuildingsV1(APITestCase):
    def createBuildings():
        Building.objects.create(building_code="ALRD", building_name="Allard Hall")
        Building.objects.create(building_code="SWNG", building_name="West Mall Swing Space")

    def testGetStatusOk(self):
        TestBuildingsV1.createBuildings()
        response = self.client.get('buildings/UBCV')
        self.assertTrue(status.is_success(response.status_code))

    def testGetStatusNotFound(self):
        response = self.client.get('buildings/UBCV')
        self.assertTrue(status.is_client_error(response.status_code))

    def testGetStatusBadRequest(self):
        TestBuildingsV1.createBuildings()
        response = self.client.get('buildings/UBCO')
        self.assertTrue(status.is_client_error(response.status_code))

    def testPostStatusMethodNotAllowed(self):
        TestBuildingsV1.createBuildings()
        response = self.client.post('buildings/UBCV')
        self.assertTrue(status.is_client_error(response.status_code))