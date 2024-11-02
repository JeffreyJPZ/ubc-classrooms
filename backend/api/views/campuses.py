"""
Views for campuses
"""
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.campuses_serializers import *
from api.models.building import *

# Version 1

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def campuses_v1(request : Request) -> Response:
    # Get all campuses

    if request.method == 'GET':
        # Query campus table and serialize query result
        campuses = list(Campus.objects.all().values("campus_code", "campus_name"))
        campuses_serializer = CampusSerializer(data=campuses, many=True)

        # Validate result and return HTTP 400 response if result is invalid
        campuses_serializer.is_valid(raise_exception=True)
        
        content = campuses_serializer.validated_data

        return Response(content, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)