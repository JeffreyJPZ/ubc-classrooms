"""
URL configuration for timeslots API
"""
from django.urls import path, register_converter

import converters

register_converter(converters.DateConverter, "date")

urlpatterns = [
    # Version 1
    path('v1/buildings/<campus:campus>/', 'TODO'),
    path('v1/roomtypes/<campus:campus>/', 'TODO'),
    path('v1/timeslots/<campus:campus>/<date:date>/<buildings:buildings>/<roomtypes:roomtypes>/<time:start>/<time:end>/', 'TODO'),
]
