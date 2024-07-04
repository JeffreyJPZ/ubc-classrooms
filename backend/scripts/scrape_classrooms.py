"""
Scrapes the classroom schedules from UBC Online Timetable and outputs the raw data in csv format
"""

import re
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException

from utils.timetable import TimetableSettings, BuildingCodeToTimetableName
from utils.targets import Targets
from utils.ubc import ClassroomType



def get_driver():
    # Creates and returns the web driver

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver



def get_classroom_type_button_id(classroom_type : ClassroomType) -> str:
    # Returns a string representing the button id for the given classroom type
    match classroom_type:
        case ClassroomType.GENERAL:
            return "LinkBtn_locationByZone"
        case ClassroomType.RESTRICTED:
            return "LinkBtn_locationRestricted"
    


def get_timetable_options(classrooms : list[str], weeks : list[str], days : list[str], period : list[str], report_type : list[str]) -> dict[str, list[str]]:
    # Returns a dictionary with the timetable select element ids mapped to the desired selections
    options = {
                'dlObject': classrooms,                                     # Classrooms
                'lbWeeks': weeks,                                           # Week Range
                'lbDays': days,                                             # Day Range
                'dlPeriod': period,                                         # Time Range
                'dlType': report_type                                       # Type of Report
            }
    return options



def get_classrooms_element_id() -> str:
    # Returns the id of the element containing the classrooms
    return "dlObject"



def get_view_timetable_id() -> str:
    # Returns the id of the element that enables viewing of a timetable
    return "bGetTimetable"



def set_option_selected(driver, value : str, selected : bool) -> None:
    # Sets the option element with the given value as the value specified under selected
    # Assumes value is valid

    if selected:
        driver.execute_script(f"document.querySelector(\"[value='{value}']\").selected = true")
    else:
        driver.execute_script(f"document.querySelector(\"[value='{value}']\").selected = false")



def clear_options_selected(driver, id : str) -> None:
    # Clears all selected timetable options belonging to the select field with the given id
    # Assumes id is valid

    try:
        options = driver.find_elements(By.XPATH, f"//select[@id='{id}']/option[@selected='selected']")

        for option in options:
            value = option.get_attribute("value")
            set_option_selected(driver, value, False)

    except NoSuchElementException:
        # No selected options exist
        pass



def set_options_selected(driver, options : dict[str, list[str]]) -> None:
    # For each select field with an id, sets all of the timetable options associated with the given values to be selected
    # Options is formatted as {select id: list of option values}
    # Assumes all ids are valid

    for id in options:
        # Sets all initially selected options as not selected
        clear_options_selected(driver, id)

        # Iterate through given values and set their associated timetable options as selected
        for value in options[id]:
            set_option_selected(driver, value, True)
                


def check_building_match(building_name : str, classroom_name : str) -> bool:
    # Returns true if the full building name can be found in the classroom name, false otherwise
    # classroom_name is in the format: "[building name] - Room [room number]"
    
    # Checks for building name in the first part of the classroom name
    return re.match(building_name, classroom_name) != None



def should_add_classroom(building_name : str, classroom_name : str) -> bool:
    # Returns true if the classroom should be added (i.e. it matches the building and its timetable is not empty), false otherwise
        
    # NOTE: Entry with classroom name "Wayne & William White Engineering Design Centre" has an empty timetable, should be skipped
    if building_name == BuildingCodeToTimetableName.EDC.name and re.fullmatch(building_name, classroom_name) != None:
        return False
    
    return check_building_match(building_name, classroom_name)



def format_name(building_code : str, classroom_name : str) -> str:
    # Returns the classroom name in the format: "[building code] [room number]"
    # Assumes the given classroom name is in the format: "[building name] - Room [room number]"

    # Partitions string to extract room number
    partition = classroom_name.partition(" - Room ")    # Returns tuple with 3 elements
    room_number = partition[2]

    return f"{building_code} {room_number}"



def get_matching_classrooms(driver, building_code : BuildingCodeToTimetableName) -> dict[str, str]:
    # For a given classroom type, returns classroom names mapped to numeric values in string format, where:
    #   - each classroom name is unique
    #   - each classroom belongs to the building represented by the building code
    #   - each classroom belongs to the classroom type
    #   - classroom name is in the format: "[building code] [room number]"

    matching_classrooms = {}
    all_classrooms = driver.find_elements(By.XPATH, f"//select[@id='{get_classrooms_element_id()}']/option")    # Gets list of all classrooms

    for classroom in all_classrooms:
        classroom_name = classroom.get_attribute("innerHTML")

        if should_add_classroom(building_code.value, classroom_name): # Uses full building name
            classroom_value = classroom.get_attribute("value")

            # Formats classroom name and assigns it to its value
            matching_classrooms[format_name(building_code.name, classroom_name)] = classroom_value
        
    return matching_classrooms



def get_table_headers() -> dict[str, int]:
    # Return a mapping of attributes for a classroom booking within an academic year to their column index in the scraped table:
    # Campus:                   UBCV
    # Year:                     Academic year in format YYYY-YYYY
    # BuildingCode:             3-5 letter code representing a building
    # Room:                     3-4 digit classroom number
    # RoomType:                 String representing whether the room the booking is in is a general teaching space or a restricted space
    # Date:                     ISO-8601 compliant date in format YYYY-MM-DD
    # Start:                    Time in 24-hour format representing the beginning of a booking
    # End:                      Time in 24-hour format representing the end of a booking
    # BookingType:              Code representing the purpose of a booking (e.g. LEC, SEM, LAB)
    # Department:               Code representing the department that the booking was made under
    # Booking:                  Full name of the booking
    # Module (optional):        Code representing the course name of a booking (if the booking is part of a course)
    # Section (optional):       Code representing the section number of a booking (if the booking is part of a course)
    # Staff (optional):         Name of the staff associated with the booking (if the booking is part of a course)
    return {
        "Campus": 0, 
        "Year": 1,
        "BuildingCode": 2, 
        "Room": 3, 
        "RoomType": 4,
        "Date": 5,
        "Start": 6,
        "End": 7,
        "BookingType": 8,
        "Department": 9,
        "Booking": 10,
        "Module": 11,
        "Section": 12,
        "Staff": 13
    }



def get_date(start_date : str, week : int, day : int) -> str:
    # Given a starting date, a week number, and a day number representing the day of the week, returns the appropriate date string in format YYYY-MM-DD (ISO-8601)
    # Assumes start date is in the format YYYY-MM-DD, and that week 1 contains the start date
    # Assumes week number is between 1-53, and day number is between 1-7 (ISO-8601)
    # Assumes week begins on a Monday

    start_datetime = datetime.strptime(start_date, TimetableSettings.FORMAT_DATE)

    # Subtract 1 from week number and day number to obtain week delta and day delta
    delta = timedelta(weeks=week-1, days=day-1)

    # Obtain date by adding delta to the start date
    date = start_datetime + delta

    return date.strftime(TimetableSettings.FORMAT_DATE)



def get_weekdays_to_day_numbers() -> dict[str, int]:
    # Returns a mapping of abbreviated weekdays to their day numbers according to ISO-8601
    return {
        "Mon": 1,
        "Tue": 2,
        "Wed": 3,
        "Thu": 4,
        "Fri": 5,
        "Sat": 6,
        "Sun": 7
    }



def get_table_headers_to_column_titles() -> dict[str, str]:
    # Returns a one-to-one mapping of a subset of table headers for the scraped table to column titles in a timetable

    return {
        "Booking": "Name",                          # Corresponds to "Name" column title in timetable
        "Section": "Section ID",                    # Corresponds to "Section ID" column
        "BookingType": "Type",                      # Corresponds to "Type" column
        "Department": "Name of Department",         # Corresponds to "Name of Department" column
        "Staff": "Staff",                           # Corresponds to "Staff" column
        "Module": "Module",                         # Corresponds to "Module" column
        "Start": "Start Time",                      # Corresponds to "Start Time" column
        "End": "End Time"                           # Corresponds to "End Time" column
    }



def get_weeks(weeks : str) -> list[int]:
    # Given a string of week numbers separated by commas and hyphens, returns all the week numbers in the string's total range
    # E.g. for a string "24, 28-31, 33", the result should be [24, 28, 29, 30, 31, 33]

    week_numbers = []
    week_ranges = weeks.split(", ")

    for weeks in week_ranges:
        # Check if each week range contains a hyphen
        if re.search("-", weeks) != None:
            weeks_partition = weeks.partition("-")

            min_week = int(weeks_partition[0])
            max_week = int(weeks_partition[2])

            # Creates list of all week numbers from min to max inclusive
            min_max_range = list(range(min_week, max_week + 1))

            week_numbers.extend(min_max_range)
        else:
            week_numbers.append(int(weeks))

    return week_numbers



def create_table_row(booking_data : dict[str, str], week : int, day : int, classroom_type : ClassroomType) -> list[str]:
    # Given the booking cell data for a given week number and weekday, process and return a booking that includes the appropriate date, with data in the order specified by get_table_headers

    # Get utilities
    table_headers = get_table_headers()
    table_headers_to_column_titles = get_table_headers_to_column_titles()

    # Initialize row size
    row = [None] * len(table_headers)

    # Create object to store processed booking data (must have same keys as specified by get_table_headers)
    processed_booking_data = {}


    # Set constant and given values in advance
    processed_booking_data["Campus"] = TimetableSettings.CAMPUS
    processed_booking_data["Year"] = TimetableSettings.ACADEMIC_YEAR
    processed_booking_data["RoomType"] = classroom_type.value

    # PROCESSING:
    # Separate location into building code and room number
    partition = booking_data["Location"].partition(" ")
    processed_booking_data["BuildingCode"] = partition[0]
    processed_booking_data["Room"] = partition[2]

    # Calculate date of the booking using reference date
    processed_booking_data["Date"] = get_date(TimetableSettings.REFERENCE_DATE, week, day)


    # Copy over booking cell data that was not set/processed (already had a one-to-one correspondence with scraped table)
    for header in table_headers_to_column_titles:
        processed_booking_data[header] = booking_data[table_headers_to_column_titles[header]]
            

    # Append processed booking cell data in the correct order
    for header in table_headers:
        row[table_headers[header]] = processed_booking_data[header]

    return row



def create_table_rows(bookings, day : int, classroom_type : ClassroomType) -> list[list[str]]:
    # For each row (booking) in the timetable, return the booking as multiple individual bookings, one for each date

    rows = []

    # Get column titles for the timetable - see get_column_titles_to_table_headers for the exact titles
    # NOTE: i-th element of column titles corresponds to the i-th booking cell for each booking
    column_titles = list(map(lambda e : e.get_text(), bookings[0].find_all("td", recursive=False)))

    # Go through each timetable row (room booking for a given weekday and a number of weeks), excluding the column titles as the first row
    for i in range(1, len(bookings)):

        # List of table data elements
        booking_cells = bookings[i].find_all("td", recursive=False)

        # Map column titles for each data cell to the data within the cell
        booking_data = {}
        for j in range(0, len(booking_cells)):
            booking_data[column_titles[j]] = booking_cells[j].get_text()

        # Get all week numbers for a bookings
        weeks = get_weeks(booking_data["Weeks"])

        # Create one row for each desired week on the given weekday
        for week in weeks:
            rows.append(create_table_row(booking_data, week, day, classroom_type))

    return rows



def scrape_classrooms(soup, classroom_type : ClassroomType) -> list[list[str]]:
    # Goes through all timetables for the selected classrooms, and:
    # For each booking, if the booking's location matches one of the given classrooms, and if no entries already exist for the location:
    # - Creates a date for each day and week specified under the booking using the start date
    # - Creates a list entry for the booking under each date
    # Returns the bookings

    # List of all timetable bookings for a building
    data = []

    # Get utilities
    weekdays_to_day_numbers = get_weekdays_to_day_numbers()

    # Get parent elements of timetable bookings
    timetables = list(map(lambda e : e.find("tbody", recursive=False), soup.find_all(class_="spreadsheet")))
        
    # Get abbreviated weekdays associated with each timetable
    # NOTE: the i-th element of timetables is the timetable for the weekday given by the i-th element of timetable_weekdays 
    timetable_weekdays = list(map(lambda e : e.get_text(), soup.find_all(class_="labelone")))

    # Go through each timetable and create table rows for each of the bookings
    for i in range(0, len(timetables)):
        
        # Skips timetable if it is empty
        if timetables[i] == None:
            continue
         
        bookings = timetables[i].find_all("tr", recursive=False)

        # Get day number for abbreviated weekday associated with timetable
        day = weekdays_to_day_numbers[timetable_weekdays[i]]

        # Store created rows
        rows = create_table_rows(bookings, day, classroom_type)
        data.extend(rows)

    return data
            


def view_timetable(driver) -> None:
    # Clicks on the button to view timetable and navigates to the timetable

    driver.find_element(By.ID, get_view_timetable_id()).click()
    driver.get(TimetableSettings.URL + 'showtimetable.aspx')



def scrape_classroom_type(driver, building_code : BuildingCodeToTimetableName, classroom_type : ClassroomType) -> list[list[str]]:
    # Sets all classrooms for a given building and classroom type as selected and returns the scraped bookings

    # Gets classroom values and names matching building code and classroom type
    classrooms = get_matching_classrooms(driver, building_code)

    # Get chosen timetable options including classrooms
    # Unpacking is faster for small collections
    options = get_timetable_options(classrooms=[*classrooms.values()], weeks=["t", "n"], days=["1-7"], period=["0-30"], report_type=["textspreadsheet;swsurl;UBCSWSActivities_TS"])

    # Sets the chosen timetable options to be selected
    set_options_selected(driver, options)

    # Navigate to timetable
    view_timetable(driver)

    # Gets parse tree for timetable page
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Scrape timetable for the given classrooms
    # Using parse tree is much faster than selenium which uses JSON wire protocol for each request (i.e. for each command)
    classroom_type_data = scrape_classrooms(soup, classroom_type)

    # Return to classrooms page
    driver.get(TimetableSettings.URL)

    return classroom_type_data
        


def create_dataframe(data : list[list[str]]) -> pd.DataFrame:
    # Returns a dataframe with the given data, and datestrings converted to datetimes

    # Ensure that scraped table columns are in the correct order
    table_headers = get_table_headers()
    # Initialize number of columns
    columns = [None] * len(table_headers)
    for header in table_headers:
        # Inserts the header at the correct index
        columns[table_headers[header]] = header

    # Initialize table for booking data
    df = pd.DataFrame(data=data, columns=columns)

    # Convert all datestrings to datetimes
    df["Date"] = pd.to_datetime(df["Date"], format=TimetableSettings.FORMAT_DATE)

    return df



def filter_bookings(dataframe : pd.DataFrame, building_code : BuildingCodeToTimetableName) -> pd.DataFrame:
    # Returns a modified dataframe with duplicate and out-of-range bookings removed
    # Assumes dataframe has columns specified in get_table_headers

    # Filter out bookings that do not belong to the building
    dataframe = dataframe[dataframe["BuildingCode"] == building_code.name]
    
    # Get start and end dates as datetimes
    start_date = datetime.strptime(TimetableSettings.START_DATE, TimetableSettings.FORMAT_DATE)
    end_date = datetime.strptime(TimetableSettings.END_DATE, TimetableSettings.FORMAT_DATE)

    # Filter out bookings that are outside of the timetable range
    dataframe = dataframe[(dataframe["Date"] >= start_date) & (dataframe["Date"] <= end_date)]

    # Filter out bookings that are duplicates (date, time, and location all overlap)
    # Keep the first instances
    dataframe = dataframe.drop_duplicates(subset=["BuildingCode", "Room", "Date", "Start", "End"], ignore_index=True)

    return dataframe



def write_to_file(dataframe : pd.DataFrame, building_code : BuildingCodeToTimetableName) -> None:
    # Writes the given data to file

    # Make path and create parent directories if they do not exist
    path = Path.cwd() / f'{Targets.RAW_BOOKING_DATA}' / f'{TimetableSettings.CAMPUS}' / f'{TimetableSettings.ACADEMIC_YEAR}' / f'{TimetableSettings.START_DATE}' / f'{TimetableSettings.CAMPUS}_{TimetableSettings.ACADEMIC_YEAR}_{TimetableSettings.START_DATE}_{building_code.name}.csv'
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write booking data to file for building in target directory
    dataframe.to_csv(path, index=False, mode="w", date_format=TimetableSettings.FORMAT_DATE)



def scrape(driver, building_code : BuildingCodeToTimetableName) -> None:
    # Scrapes all classroom bookings for a building and writes the data to file

    # List of all timetable bookings for a building
    data = []

    # Navigate to general or restricted classrooms page
    for classroom_type in ClassroomType:
        
        button_id = get_classroom_type_button_id(classroom_type)
        driver.find_element(By.ID, button_id).click()

        # Get a subtable of all the classroom bookings for a classroom type
        classroom_type_data = scrape_classroom_type(driver, building_code, classroom_type)

        data.extend(classroom_type_data)

    df = filter_bookings(create_dataframe(data), building_code)

    write_to_file(df, building_code)



def main() -> None:
    # Scrapes and writes the classroom booking data to file

    # Navigate to UBC Online Timetable main page
    driver = get_driver()
    driver.get(TimetableSettings.URL)

    # Scrape all classrooms in each building
    for building_code in BuildingCodeToTimetableName:
        scrape(driver, building_code)



if __name__ == "__main__":
    main()


