"""
Uses the raw booking data to calculate available timeslots for classrooms throughout the academic year
"""

import pandas as pd
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path

from models import TimetableSettings



TARGET_DIR = '/timeslot_data' # Directory to write files to