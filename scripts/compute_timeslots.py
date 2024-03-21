"""
Uses the raw booking data to calculate available timeslots for classrooms throughout the academic year
Assumes that the raw booking directory for the academic year in TimetableSettings has already been populated with the buildings specified in the config file
"""
import json
import pandas as pd
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path

from models import TimetableSettings
from models import Targets
from models import BuildingCode



def get_table_headers() -> dict[str, int]:
    # Return a mapping of attributes for an available timeslot within an academic year to their column index in the timeslot table:
    # Campus:                   UBCV
    # Year:                     Academic year in format YYYY-YYYY
    # Building:                 3-5 letter code representing a building
    # Room:                     3-4 digit classroom number
    # RoomType:                 String representing whether the room the is a general teaching space or a restricted space
    # Start:                    Datetime in ISO-8601 format representing the beginning of the timeslot
    # End:                      Datetime in ISO-8601 format representing the end of the timeslot
    return {
        "Campus": 0, 
        "Year": 1,
        "Building": 2, 
        "Room": 3, 
        "RoomType": 4,
        "Start": 5,
        "End": 6
    }



def compute_timeslots_by_rooms(dataframe, building_code : BuildingCode) -> list[list[str]]:
    return []



def write_to_file(data : list[str[str]], building_code : BuildingCode) -> None:
    # Writes the timeslot data to file

    # Ensure that scraped table columns are in the correct order
    table_headers = get_table_headers()
    # Initialize number of columns
    columns = [None] * len(table_headers)
    for header in table_headers:
        # Inserts the header at the correct index
        columns[table_headers[header]] = header

    # Initialize table for timeslot data
    df = pd.DataFrame(data=data, columns=columns)

    # Make path and create parent directories if they do not exist
    path = Path.cwd() / f'{Targets.TIMESLOT_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{building_code.name}.csv'
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write timeslot data to file for building in target directory
    df.to_csv(path, index=False, mode="w")



def compute_timeslots(building_code : BuildingCode) -> None:
    # Reads booking data from file for a building, gets the available timeslots for the entire academic year, and writes the timeslots to file

    # Get path to booking data file
    read_path = Path.cwd() / f'{Targets.RAW_BOOKING_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{building_code.name}.csv'

    # Read file into dataframe and convert datestrings into datetimes
    df = pd.read_csv(read_path, parse_dates=["Date"], date_format="%Y-%m-%d")

    # Get all available timeslots for the building
    timeslots = compute_timeslots_by_rooms(df, building_code)

    # Write timeslots to file
    write_to_file(timeslots, building_code)



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

    # TODO: replace with compute_timeslots_config for prod
    configPath = 'config/compute_timeslots_config_test.json'

    with open(Path(__file__).parent / configPath, encoding='utf8') as f:
        building_code_data = json.load(f)

        # Validate building codes
        for building_code in building_code_data['buildingCodes']:
            try:
                assert building_code == BuildingCode[building_code].name
            except AssertionError:
                print("An invalid building code was entered\n")
                return

        for building_code in building_code_data['buildingCodes']:
            compute_timeslots(BuildingCode[building_code])
        


main()