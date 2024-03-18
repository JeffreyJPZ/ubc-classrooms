"""
Scrapes the classroom schedules from UBC Online Timetable and outputs the raw data in csv format
"""

import json
import re
import pandas as pd
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException

from models import BuildingCode



URL = 'https://sws-van.as.it.ubc.ca/sws_2023/' # Change date to get updated timetable
CAMPUS = "UBCV"



class ClassroomType(Enum):
    # Types of classrooms - "General Teaching Space" is for general teaching spaces that are open to all faculties, 
    #                       "Restricted Space" is for restricted spaces primarily reserved for a respective faculty
    GENERAL = "General Teaching Space"
    RESTRICTED = "Restricted Space"



def get_driver():
    # Creates and returns the Chrome web driver

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
    if building_name == BuildingCode.EDC.name and re.fullmatch(building_name, classroom_name) != None:
        return False
    
    return check_building_match(building_name, classroom_name)



def format_name(building_code : str, classroom_name : str) -> str:
    # Returns the classroom name in the format: "[building code] [room number]"
    # Assumes the given classroom name is in the format: "[building name] - Room [room number]"

    # Partitions string to extract room number
    partition = classroom_name.partition(" - Room ")    # Returns tuple with 3 elements
    room_number = partition[2]

    return f"{building_code} {room_number}"



def get_matching_classrooms(driver, building_code : BuildingCode) -> dict[str, str]:
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



def get_table_headers() -> list[str]:
    # Return a list of attributes for a classroom booking within an academic year in the following order:
    # Campus:                   UBCV
    # Year:                     Academic year in format 20XX-XX
    # Building:                 3-5 letter code representing a building
    # Room:                     3-4 digit classroom number
    # RoomType:                 String representing whether the room the booking is in is a general teaching space or a restricted space
    # Date:                     ISO-8601 compliant date in format YYYY-MM-DD
    # Start:                    Time in 24-hour format representing the beginning of a booking
    # End:                      Time in 24-hour format representing the end of a booking
    # Type:                     Code representing the purpose of a booking (e.g. LEC, SEM, LAB)
    # Department:               Code representing the department that the booking was made under
    # Booking:                  Full name of the booking
    # Module (optional):        Code representing the course name of a booking (if the booking is part of a course)
    # Section (optional):       Code representing the section number of a booking (if the booking is part of a course)
    # Staff (optional):         Name of the staff associated with the booking (if the booking is part of a course)
    return ["Campus", "Year", "Building", "Room", "RoomType", "Date", "Start", "End", "Type", "Department", "Booking", "Module", "Section", "Staff"]



def get_date(start_date : str, week : int, day : int) -> str:
    # Given a starting date, a week number, and a day number representing the day of the week, returns the appropriate date string in format YYYY-MM-DD
    # Assumes start date is in the format MM/DD/YYYY
    # Assumes week number is between 1-53, and day number is between 1-7 (ISO-8601)
    # Assumes week begins on a Monday

    start_datetime = datetime.strptime(start_date, "%m/%d/%Y")

    # Subtract 1 from week number and day number to obtain week delta and day delta
    delta = timedelta(weeks=week-1, days=day-1)

    # Obtain date by adding delta to the start date
    date = start_datetime + delta

    return date.strftime("%Y-%m-%d")



def get_start_date(soup) -> str:
    # Returns the start date for all timetables in format MM/DD/YYYY

    start_date = soup.find(class_="header-0-0-3").get_text()

    # Replace abbreviated year in start date with full year
    formatted_start_date = start_date[:-2] + "20" + start_date[-2:]

    return formatted_start_date



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



def get_column_indices_to_table_headers() -> dict[int, str]:
    # Returns a mapping of column indices for a timetable to table headers for the scraped table
    # If there is a one-to-many correspondance between a column in the timetable and table headers,
    # then the table header ordering specified by get_table_headers determines the ordering of the table headers
    # NOTE: Weeks and Day are combined into one Date column in the scraped table

    return {
        0: ["Booking"],             # Corresponds to "Name" column
        1: ["Section"],             # Corresponds to "Section ID" column
        2: ["Type"],                # Corresponds to "Type" column
        3: ["Department"],          # Corresponds to "Name of Department" column
        4: ["Date"],                # Corresponds to "Weeks" column
        5: ["Building", "Room"],    # Corresponds to "Location" column
        6: ["Staff"],               # Corresponds to "Staff" column
        7: ["Module"],              # Corresponds to "Module" column
        8: ["Date"],                # Corresponds to "Day" column
        9: ["Start"],               # Corresponds to "Start Time" column
        10: ["End"]                 # Corresponds to "End Time" column
    }



def scrape_classrooms(soup, classrooms : dict[str, str], classroom_type : ClassroomType) -> None:
    # Goes through all timetables for the selected classrooms, and:
    # For each booking, if the booking's location matches one of the given classrooms, and if no entries already exist for the location:
    # - Creates a date for each day and week specified under the booking using the start date
    # - Creates a table entry for the booking under each date
    # - Outputs the table in csv format
    
    # Initialize scraped table
    df = pd.DataFrame(columns=get_table_headers())

    # Get utilities
    start_date = get_start_date(soup)
    weekdays_to_day_numbers = get_weekdays_to_day_numbers()
    column_indices_to_table_headers = get_column_indices_to_table_headers()

    # Get parent elements of timetable bookings
    timetables = map(lambda e : e.find("tbody", recursive=False), soup.find_all(class_="spreadsheet"))

    # Get weekdays associated with each timetable
    # NOTE: the i-th element of timetables is the timetable for the weekday given by the i-th element of timetable_weekdays 
    timetable_weekdays = map(lambda e : e.get_text(), soup.find_all(class_="labelone"))

    # Go through each timetable
    # for timetable in timetables:
        
        # print(timetable)

        # Go through each timetable row (room bookings for a given weekday and given week(s)), excluding the column titles as the first row
        # for i in range(1, len(timetable)):
        #     # Create one entry for each week and weekday
            


def view_timetable(driver) -> None:
    # Clicks on the button to view timetable and navigates to the timetable

    driver.find_element(By.ID, get_view_timetable_id()).click()
    driver.get(URL + 'showtimetable.aspx')



def scrape(driver, building_code : BuildingCode, classroom_type : ClassroomType) -> None:
    # Parses and saves all classrooms for a given building and classroom type to csv

    # Gets classroom values and names matching building code and classroom type
    classrooms = get_matching_classrooms(driver, building_code)

    # Get chosen timetable options including classrooms
    # Unpacking is faster for small collections
    options = get_timetable_options(classrooms=[*classrooms.values()], weeks=['1-53'], days=['1-7'], period=['0-10'], report_type=['textspreadsheet;swsurl;UBCSWSActivities_TS'])

    # Sets the chosen timetable options to be selected
    set_options_selected(driver, options)

    # Navigate to timetable
    view_timetable(driver)

    # Gets parse tree for timetable page
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Scrape timetable using the given classrooms
    # Using parse tree is much faster than selenium which uses JSON wire protocol for each request (i.e. for each command)
    scrape_classrooms(soup, classrooms, classroom_type)

    # Return to classrooms page
    driver.get(URL)
        


def main() -> None:
    # Scrapes and saves the classroom data to csv

    # TODO: replace with scrape_classrooms_config.json for prod
    configPath = 'config/scrape_classrooms_config_test.json'

    with open(Path(__file__).parent / configPath, encoding='utf8') as f:
        building_code_data = json.load(f)

        # Validate building codes
        for building_code in building_code_data['buildingCodes']:
            try:
                assert building_code == BuildingCode[building_code].name
            except AssertionError:
                print("An invalid building code was entered\n")
                return

        # Navigate to UBC Online Timetable main page
        driver = get_driver()
        driver.get(URL)

        # Scrape all classrooms in each building
        for building_code in building_code_data['buildingCodes']:

            # Navigate to general or restricted classrooms page
            for classroom_type in ClassroomType:
                
                button_id = get_classroom_type_button_id(classroom_type)
                driver.find_element(By.ID, button_id).click()

                # Scrape each classroom belonging to the classroom type and save to csv
                scrape(driver, BuildingCode[building_code], classroom_type)



main()


