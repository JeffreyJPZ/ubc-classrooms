"""
Views for room types
"""
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from serializers.roomtypes_serializers import *
from models.roomtype import *

# Version 1

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def roomtypes_v1(request : Request, campus : str) -> Response:
    # Get all room types for a campus

    if request.method == 'GET':
        path_serializer = PathParametersSerializer(data=campus)

        # Validate path and return HTTP 400 response if path is invalid
        try:
            path_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(path_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Query roomtypes table and serialize query result
        roomtypes = RoomType.objects.all()
        roomtypes_serializer = RoomTypeSerializer(data=roomtypes)

        # Validate result and return HTTP 400 response if result is invalid
        try:
            roomtypes_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(roomtypes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        content = roomtypes_serializer.data

        return Response(content, status=status.HTTP_200_OK) if content != [] else Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)