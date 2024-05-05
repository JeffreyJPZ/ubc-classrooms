"""
Views for timeslots
"""
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from serializers.timeslots_serializers import *
from models.timeslot import *

# Version 1

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def timeslots_v1(request : Request, campus : str) -> Response:
    # Get timeslots for empty classrooms matching given query params for a campus

    if request.method == 'GET':
        path_serializer = PathParametersSerializer(data=campus)

        # Validate path and return HTTP 400 response if path is invalid
        try:
            path_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(path_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query_params_serializer = QueryParametersSerializer(data=request.query_params)

        # Validate query params and return HTTP 400 response if query params are invalid
        try:
            query_params_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(query_params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        params = query_params_serializer.validated_data

        # Query timeslots table and serialize query result
        timeslots = Timeslot.objects.filter(campus=campus,
                                            building_code=params.get("buildings"),
                                            room_type=params.get("room_types"),
                                            start=params.get("date") + " " + params.get("start"),
                                            end=params.get("date") + " " + params.get("end"))
        timeslots_serializer = TimeslotSerializer(data=timeslots)

        # Validate result and return HTTP 400 response if result is invalid
        try:
            timeslots_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(timeslots_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        content = timeslots_serializer.data

        return Response(content, status=status.HTTP_200_OK) if content != [] else Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
