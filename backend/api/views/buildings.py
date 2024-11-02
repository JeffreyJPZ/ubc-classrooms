"""
Views for buildings
"""
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.buildings_serializers import *
from api.models.building import *

# Version 1

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def buildings_v1(request : Request, campus : str) -> Response:
    # Get all buildings for a campus

    if request.method == 'GET':
        # Validate path and return HTTP 404 response if resource does not exist
        path_params_serializer = PathParametersSerializer(data={"campus": campus})
        if not path_params_serializer.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        # Query joined campus and building table and serialize query result
        path_params = path_params_serializer.validated_data
        
        buildings = list(Building.objects.filter(campus__campus_code=path_params.get("campus")).values("campus_id", "building_code", "building_name"))

        # Remove id suffixes added by Django
        for building in buildings:
            building["campus"] = building["campus_id"]
            del building["campus_id"]

        buildings_serializer = BuildingSerializer(data=buildings, many=True)

        # Validate result and return HTTP 400 response if result is invalid
        buildings_serializer.is_valid(raise_exception=True)
        
        content = buildings_serializer.validated_data

        return Response(content, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)