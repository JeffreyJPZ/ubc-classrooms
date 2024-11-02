"""
API tests for roomtypes resource
"""
from rest_framework.test import APITestCase

from api.models.campus import *
from api.models.roomtype import *

# Version 1

class TestRoomtypesV1(APITestCase):
    def setUp(self):
        ubcv_campus = Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")[0]
        RoomType.objects.get_or_create(campus=ubcv_campus, room_type="General")
        RoomType.objects.get_or_create(campus=ubcv_campus, room_type="Restricted")

    def testGetStatusOk(self):
        response = self.client.get('/api/v1/roomtypes/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/roomtypes/UBCV/')
        self.assertEqual(response.status_code, 200)

    def testGetStatusNotFound(self):
        response = self.client.get('/api/v1/roomtypes/UBCA/')
        self.assertEqual(response.status_code, 404)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v1/roomtypes/UBCV/')
        self.assertEqual(response.status_code, 405)