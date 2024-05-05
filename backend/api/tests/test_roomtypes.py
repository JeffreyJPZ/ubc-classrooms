"""
API tests for roomtypes resource
"""
from rest_framework import status
from rest_framework.test import APITestCase

from models.roomtype import *

class TestRoomtypesV1(APITestCase):
    def createRoomtypes():
        RoomType.objects.create(room_type="General")
        RoomType.objects.create(room_type="Restricted")

    def testGetStatusOk(self):
        TestRoomtypesV1.createRoomtypes()
        response = self.client.get('roomtypes/UBCV')
        self.assertTrue(status.is_success(response.status_code))

    def testGetStatusNotFound(self):
        response = self.client.get('roomtypes/UBCV')
        self.assertTrue(status.is_client_error(response.status_code))

    def testGetStatusBadRequest(self):
        TestRoomtypesV1.createRoomtypes()
        response = self.client.get('roomtypes/UBCO')
        self.assertTrue(status.is_client_error(response.status_code))

    def testPostStatusMethodNotAllowed(self):
        TestRoomtypesV1.createRoomtypes()
        response = self.client.post('roomtypes/UBCV')
        self.assertTrue(status.is_client_error(response.status_code))