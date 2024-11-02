"""
API tests for campus resource
"""
from rest_framework.test import APITestCase

from api.models.campus import *

# Version 1

class TestCampusesV1(APITestCase):
    def setUp(self):
        Campus.objects.get_or_create(campus_code="UBCV", campus_name="Vancouver")

    def test_GetStatusOk(self):
        response = self.client.get('/api/v1/campuses/')
        self.assertEqual(response.status_code, 200)

    def test_GetEmptyDBStatusOk(self):
        response = self.client.get('/api/v1/campuses/')
        self.assertEqual(response.status_code, 200)

    def test_GetQueryParamsStatusOk(self):
        response = self.client.get('/api/v1/campuses/', QUERY_STRING="campus=UBCV")
        self.assertEqual(response.status_code, 200)

    def test_PostStatusMethodNotAllowed(self):
        response = self.client.post('/api/v1/campuses/')
        self.assertEqual(response.status_code, 405)