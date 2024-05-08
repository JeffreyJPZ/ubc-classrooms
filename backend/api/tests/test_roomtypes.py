"""
API tests for roomtypes resource
"""
from rest_framework.test import APITestCase

from api.models.roomtype import *

# Version 1

class TestRoomtypesV1(APITestCase):
    def createRoomtypes():
        RoomType.objects.create(campus="UBCV", room_type="General")
        RoomType.objects.create(campus="UBCV", room_type="Restricted")

    def testGetStatusOk(self):
        TestRoomtypesV1.createRoomtypes()
        response = self.client.get('/api/v1/roomtypes/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/roomtypes/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetStatusNotFound(self):
        TestRoomtypesV1.createRoomtypes()
        response = self.client.get('/api/v1/roomtypes/UBCO/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        TestRoomtypesV1.createRoomtypes()
        response = self.client.post('/api/v1/roomtypes/UBCV/')
        self.assertEqual(response.status_code, 405)