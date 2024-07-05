"""
Uses the raw booking data to calculate available timeslots for classrooms throughout the academic year
Assumes that the raw booking directory for the academic year in TimetableSettings has already been populated with the buildings specified in the config file
"""
import pandas as pd
from typing import Iterator
from datetime import datetime, timedelta
from pathlib import Path

from utils.timetable import TimetableSettings
from utils.targets import Targets
from utils.ubc import BuildingCodeToFullName



def get_timeslot_headers() -> dict[str, int]:
    # Return a mapping of attributes for an available timeslot within an academic year to their column index in the timeslot table:
    # Campus:                   UBCV
    # Year:                     Academic year in format YYYY-YYYY
    # BuildingCode:             3-5 letter code representing a building
    # BuildingName:             Full name of building
    # Room:                     3-4 digit classroom number
    # RoomType:                 String representing whether the room the is a general teaching space or a restricted space
    # Start:                    Datetime in ISO-8601 format representing the beginning of the timeslot
    # End:                      Datetime in ISO-8601 format representing the end of the timeslot
    return {
        "Campus": 0, 
        "Year": 1,
        "BuildingCode": 2,
        "BuildingName": 3,
        "Room": 4, 
        "RoomType": 5,
        "Start": 6,
        "End": 7
    }



def get_timeslot_headers_to_booking_headers() -> dict[str, str]:
    # Returns a one-to-one mapping of a subset of table headers for the timeslot table to table headers for the booking data table

    return {
        "Campus": "Campus", 
        "Year": "Year",
        "BuildingCode": "BuildingCode", 
        "Room": "Room", 
        "RoomType": "RoomType",
    }



def create_timeslot(timeslot_data : dict[str, str], start : str, end : str) -> list[str]:
    # Return a timeslot with start and end datetimes for a given room, in the order specified by get_timeslot_headers

    # Get utilities
    timeslot_headers = get_timeslot_headers()

    # Initialize timeslot size
    timeslot = [None] * len(timeslot_headers)

    # Copy over building full name
    timeslot_data["BuildingName"] = BuildingCodeToFullName[timeslot_data["BuildingCode"]].value

    # Copy over start and end datetimes
    timeslot_data["Start"] = start
    timeslot_data["End"] = end

    # Copy the timeslot data to the correct positions
    for header in timeslot_headers:
        timeslot[timeslot_headers[header]] = timeslot_data[header]

    return timeslot



def compute_timeslots_by_room_and_date(room_date_dataframe : pd.DataFrame, shared_timeslot_data : dict[str, str], date : datetime) -> list[list[str]]:
    # Create timeslots for a given room and date, from the start time to the end time given by the timetable

    room_date_timeslots = []

    # Sort bookings in increasing order by start time (as they are non-overlapping), and transpose in order to iterate over columns (efficient)
    sorted_room_date_dataframe = room_date_dataframe.sort_values(by=["Start"]).T

    # Creates ISO-8601 datetimes for start and end datetimes
    start = datetime.strptime(date.strftime(TimetableSettings.FORMAT_DATE) + " " + TimetableSettings.START_TIME, TimetableSettings.FORMAT_DATETIME)
    end = datetime.strptime(date.strftime(TimetableSettings.FORMAT_DATE) + " " + TimetableSettings.END_TIME, TimetableSettings.FORMAT_DATETIME)

    # Sets datetime to keep track of start of current timeslot
    curr = start

    # Go through bookings sorted by time for the given room and date, computing timeslots from the time intervals not occupied by a booking
    # Each column is a booking, with rows as the attributes
    for label, content in sorted_room_date_dataframe.items():

        # End immediately if the latest time has been reached
        if curr == end:
            break

        # Get start and end datetimes for a booking
        booking_start = content.get("Start")
        booking_end = content.get("End")

        # Check if current time is not the beginning of a booking - if so, create a timeslot spanning the current time to the beginning of the next booking
        if curr != booking_start:
            room_date_timeslots.append(create_timeslot(shared_timeslot_data, curr.strftime(TimetableSettings.FORMAT_DATETIME), booking_start.strftime(TimetableSettings.FORMAT_DATETIME)))

        # Jump to the end of the booking
        curr = booking_end
        

    # Guard for the case where there are no bookings for the given room and date, or if the last booking's end time is not the latest time possible
    if curr != end:
        room_date_timeslots.append(create_timeslot(shared_timeslot_data, curr.strftime(TimetableSettings.FORMAT_DATETIME), end.strftime(TimetableSettings.FORMAT_DATETIME)))
        
    return room_date_timeslots



def generate_dates(start : str, end : str) -> Iterator[datetime]:
    # Returns all the dates between the given start and end dates, inclusive
    # Credit to https://stackoverflow.com/a/70426202

    start_date = datetime.strptime(start, TimetableSettings.FORMAT_DATE)
    end_date = datetime.strptime(end, TimetableSettings.FORMAT_DATE)

    curr_date = start_date

    while curr_date <= end_date:
        yield curr_date
        curr_date += timedelta(days=1)



def compute_timeslots_by_room(room_dataframe : pd.DataFrame) -> list[list[str]]:
    # Create timeslots for the room from the start date to the end date given by the timetable
    
    room_timeslots = []

    # Generate a series of dates from the timetable's start date to end date
    dates = generate_dates(TimetableSettings.START_DATE, TimetableSettings.END_DATE)

    # Populate object with data that is common to all timeslots (one-to-one correspondence with booking data table)
    shared_timeslot_data = {}
    headers = get_timeslot_headers_to_booking_headers()
    for header in headers:
        # Use the data from the first row
        shared_timeslot_data[header] = room_dataframe.at[room_dataframe.index[0], header]

    for date in dates:
        # Query for bookings that match the given date
        room_date_dataframe = room_dataframe[room_dataframe["Date"] == date]

        # Compute timeslots for the room on the given date
        room_date_timeslots = compute_timeslots_by_room_and_date(room_date_dataframe, shared_timeslot_data, date)

        room_timeslots.extend(room_date_timeslots)

    return room_timeslots



def compute_timeslots_by_building(building_dataframe : pd.DataFrame) -> list[list[str]]:
    # Create timeslots for each unique room in the building

    building_timeslots = []

    # Get all unique rooms
    unique_rooms = pd.unique(building_dataframe["Room"])

    # Go through each room and create timeslots for the entire academic year
    for room in unique_rooms:
        # Get only bookings that match the room
        room_dataframe = building_dataframe[building_dataframe["Room"] == room]

        # Compute the timeslots for the room
        room_timeslots = compute_timeslots_by_room(room_dataframe)

        building_timeslots.extend(room_timeslots)

    return building_timeslots



def read_from_file(building_code : BuildingCodeToFullName) -> pd.DataFrame:
    # Reads the booking data for the building from file and returns a dataframe with the booking data

    # Get path to booking data file
    read_path = Path.cwd() / f'{Targets.RAW_BOOKING_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{TimetableSettings.START_DATE}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{TimetableSettings.START_DATE}_{building_code.name}.csv'

    # Read file into dataframe
    df = pd.read_csv(read_path, index_col=False)

    return df



def write_to_file(data : list[list[str]], building_code : BuildingCodeToFullName) -> None:
    # Writes the timeslot data to file

    # Ensure that scraped table columns are in the correct order
    table_headers = get_timeslot_headers()
    # Initialize number of columns
    columns = [None] * len(table_headers)
    for header in table_headers:
        # Inserts the header at the correct index
        columns[table_headers[header]] = header

    # Initialize table for timeslot data
    df = pd.DataFrame(data=data, columns=columns)

    # Make path and create parent directories if they do not exist
    path = Path.cwd() / f'{Targets.TIMESLOT_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{TimetableSettings.START_DATE}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{TimetableSettings.START_DATE}_{building_code.name}.csv'
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write timeslot data to file for building in target directory
    df.to_csv(path, index=False, mode="w")



def compute_timeslots(building_code : BuildingCodeToFullName) -> None:
    # Reads booking data from file for a building, gets the available timeslots for the entire academic year, and writes the timeslots to file
    df = read_from_file(building_code)

    # Convert datestrings and timestrings into ISO-8601 datetimes
    df["Start"] = pd.to_datetime(df["Date"] + " " + df["Start"], format=TimetableSettings.FORMAT_DATETIME)
    df["End"] = pd.to_datetime(df["Date"] + " " + df["End"], format=TimetableSettings.FORMAT_DATETIME)
    df["Date"] = pd.to_datetime(df["Date"], format=TimetableSettings.FORMAT_DATE)

    # Get all available timeslots for the building
    data = compute_timeslots_by_building(df)

    write_to_file(data, building_code)



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

    for building_code in BuildingCodeToFullName:
        compute_timeslots(building_code)
        
        
        

if __name__ == "__main__":
    main()