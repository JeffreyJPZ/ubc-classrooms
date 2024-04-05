"""
Views for buildings
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


# Version 1

@api_view(['GET'])
def buildings_v1(request : Request, campus : str):
    # Get buildings
    
    result = [] # stub
    if result == []:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response('hi', status=status.HTTP_200_OK)