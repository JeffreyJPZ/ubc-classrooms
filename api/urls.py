"""
URL configuration for timeslots API
"""
from django.urls import path, register_converter

import converters

register_converter(converters.DateConverter, "date")

urlpatterns = [
    # Version 1
    path('v1/buildings/<str:campus>/', 'TODO'),
    path('v1/roomtypes/<str:campus>/', 'TODO'),
    path('v1/timeslots/<str:campus>/<date:date>/', 'TODO'),
    
    # Use query params for start time, end time, building names, and room types
]
