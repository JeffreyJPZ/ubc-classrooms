"""
API tests for campus resource
"""
from rest_framework.test import APITestCase

from .utils import BytestoString
from api.models.campus import *

# Version 1

class CampusesResponseV1:
    response_data = [
        {"campus_code": "UBCV", "campus_name": "Vancouver"},
        {"campus_code": "UBCO", "campus_name": "Okanagan"}
    ]

class TestCampusesV1(APITestCase):
    def setUp(self):
        Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")
        Campus.objects.get_or_create(campus_code="UBCO", campus_name="Okanagan")

    def testGetStatusOk(self):
        response = self.client.get('/api/v1/campuses/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), CampusesResponseV1.response_data)

    def testGetQueryParamsStatusOk(self):
        response = self.client.get('/api/v1/campuses/', QUERY_STRING="campus=UBCV")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(BytestoString(response.content), CampusesResponseV1.response_data)

    def testPostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v1/campuses/')
        self.assertEqual(response.status_code, 405)