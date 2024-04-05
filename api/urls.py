"""
URL configuration for timeslots API
"""
from django.urls import path, register_converter
from views import buildings, roomtypes, timeslots

import converters

register_converter(converters.DateConverter, "date")

urlpatterns = [
    # Version 1
    path('v1/buildings/<str:campus>/', buildings.buildings_v1),
    path('v1/roomtypes/<str:campus>/', roomtypes.roomtypes_v1),
    path('v1/timeslots/<str:campus>/<date:date>/', timeslots.timeslots_v1),
]
