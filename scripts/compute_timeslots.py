"""
Uses the raw booking data to calculate available timeslots for classrooms throughout the academic year
"""

import pandas as pd
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path

from models import TimetableSettings



TARGET_DIR = '/timeslot_data' # Directory to write files to



def main() -> None:
    # Reads booking data from file for the desired buildings, and for each building:
    # - Get all of the rooms in the building
    # - For each room:
    #   - Get all of the bookings for the room on a certain date, from the start date to the end date given by the timetable
    #   - Create timeslots where:
    #       - The timeslots are within the range given by the timetable [07:00, 22:00]
    #       - The start and end of each timeslot may be at a half-hour mark (XX:30), or an hour mark (XX:00)
    #       - Each timeslot spans the largest continuous interval possible between the end of one booking and the start of another booking
    #       - No two timeslots overlap
    # Writes the timeslot data to file
    
    return 0 # stub



main()