"""
Views for timeslots
"""
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from datetime import datetime

from api.serializers.timeslots_serializers import *
from api.models.timeslot import *

# Version 1

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def timeslots_v1(request : Request, campus : str) -> Response:
    # Get timeslots for empty classrooms matching given query query_params for a campus

    if request.method == 'GET':
        # Validate path and return HTTP 404 response if resource does not exist
        path_params_serializer = PathParametersSerializer(data={"campus": campus})
        if not path_params_serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Create mapping of all valid query params
        valid_query_params = {
           "date": True,
           "start": True,
           "end": True,
           "buildings": True,
           "room_types": True
        }

        # Validate query params and return HTTP 400 response if query params are invalid
        for query_param in request.query_params:
            try:
                assert valid_query_params[query_param] == True
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        query_params_serializer = QueryParametersSerializer(data={
           "date": request.query_params.get("date"),
           "start": request.query_params.get("start"),
           "end": request.query_params.get("end"),
           "buildings": request.query_params.getlist("buildings"),
           "room_types": request.query_params.getlist("room_types")
        })
        query_params_serializer.is_valid(raise_exception=True)
    
        # Query timeslots table
        path_params = path_params_serializer.validated_data
        query_params = query_params_serializer.validated_data

        timeslots = Timeslot.objects.filter(campus=path_params.get("campus"))
        
        # Check if optional query_params are not null or empty and query
        if query_params.get("date"):
            if query_params.get("start") and query_params.get("end"):
                timeslots = timeslots.filter(start__lte=datetime.combine(query_params.get("date"), query_params.get("start")),
                                             end__gte=datetime.combine(query_params.get("date"), query_params.get("end")))
            if query_params.get("start"):
                timeslots = timeslots.filter(start__lte=datetime.combine(query_params.get("date"), query_params.get("start")),
                                             end__date=query_params.get("date"))
            if query_params.get("end"):
                timeslots = timeslots.filter(start__date=query_params.get("date"),
                                             end__gte=datetime.combine(query_params.get("date"), query_params.get("end")))
            timeslots = timeslots.filter(start__date=query_params.get("date"))
        if query_params.get("buildings"):
            timeslots = timeslots.filter(building_code__in=query_params.get("buildings"))
        if query_params.get("room_types"):
            timeslots = timeslots.filter(room_type__in=query_params.get("room_types"))

        # Add column for date to all timeslots, and truncate start and end
        timeslots = list(timeslots.values())
        for t in timeslots:
            t["date"] = t["start"].date()
            t["start"] = t["start"].time()
            t["end"] = t["end"].time()

        # Serialize query result
        timeslots_serializer = TimeslotSerializer(data=timeslots, many=True)

        # Validate result and return HTTP 400 response if result is invalid
        timeslots_serializer.is_valid(raise_exception=True)
        
        content = timeslots_serializer.validated_data

        return Response(content, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
