"""
URL configuration for UBC Classrooms API
"""
from django.urls import path
from .views import campuses, buildings, roomtypes, timeslots

urlpatterns = [
    # Version 1
    path('v1/campuses/', campuses.campuses_v1),
    path('v1/buildings/<str:campus>/', buildings.buildings_v1),
    path('v1/roomtypes/<str:campus>/', roomtypes.roomtypes_v1),
    path('v1/timeslots/<str:campus>/', timeslots.timeslots_v1),

    # Version 2
    path('v2/buildings/<str:campus>/', buildings.buildings_v2)
]
