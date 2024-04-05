"""
Views for room types
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

# Version 1

@api_view(['GET'])
def roomtypes_v1(request : Request, campus : str):
    # Get room types

    result = [] # stub
    if result == []:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response('hi')