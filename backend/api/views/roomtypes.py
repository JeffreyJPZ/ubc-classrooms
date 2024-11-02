"""
Views for room types
"""
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.roomtypes_serializers import *
from api.models.roomtype import *

# Version 1

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def roomtypes_v1(request : Request, campus : str) -> Response:
    # Get all room types for a campus

    if request.method == 'GET':
        # Validate path and return HTTP 404 response if resource does not exist
        path_params_serializer = PathParametersSerializer(data={"campus": campus})
        if not path_params_serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Deserialize path params
        path_params = path_params_serializer.validated_data

        # Query joined campus and roomtype table and serialize query result
        roomtypes = list(RoomType.objects.filter(campus__campus_code=path_params.get("campus")).values("campus_id", "room_type"))

        # Remove id suffix added by Django
        for roomtype in roomtypes:
            roomtype["campus"] = roomtype["campus_id"]
            del roomtype["campus_id"]

        roomtypes_serializer = RoomTypeSerializer(data=roomtypes, many=True)

        # Validate result and return HTTP 400 response if result is invalid
        roomtypes_serializer.is_valid(raise_exception=True)
        
        content = roomtypes_serializer.validated_data

        return Response(content, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)