"""
Views for timeslots
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from datetime import date

# Version 1

@api_view(['GET'])
def timeslots_v1(request : Request, campus : str, date : date):
    # Get timeslots for empty classrooms

    # Use query params for start time, end time, building names, and room types
    result = [] # stub
    if result == []:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response('hi')
