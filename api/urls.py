"""
URL configuration for timeslots API
"""
from django.urls import path
from views import buildings, roomtypes, timeslots

urlpatterns = [
    # Version 1
    path('v1/buildings/<str:campus>/', buildings.buildings_v1),
    path('v1/roomtypes/<str:campus>/', roomtypes.roomtypes_v1),
    path('v1/timeslots/<str:campus>/', timeslots.timeslots_v1),
]
