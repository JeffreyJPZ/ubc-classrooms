"""
Scrapes the classroom schedules from UBC Online Timetable and outputs the raw data in csv format
"""

import json
import re
import pandas as pd
from enum import Enum
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException

from models import BuildingCode



url = 'https://sws-van.as.it.ubc.ca/sws_2023/'
campus = "UBCV"



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
    


def get_timetable_options() -> dict[str, list[str]]:
    # Returns a dictionary with the timetable options mapped to the most comprehensive values
    options = {
                'lbWeeks': ['1-53'],                                        # Week Range - All Weeks
                'lbDays': ['1-7'],                                          # Day Range - All Days
                'dlPeriod': ['0-10'],                                       # Time Range - All Day 07:00-22:00
                'dlType': ['individual;swsurl;UBCSWSLocationIndividual']    # Type of Report - Single (Basic)
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
    # Returns true if the building name can be found in the classroom name, false otherwise
    # classroom_name is in the format: "[building name] - [room number]"
    
    # Checks for building name in the first part of the classroom name
    return re.match(building_name, classroom_name) != None



def should_add_classroom(building_name : str, classroom_name : str) -> bool:
    # Returns true if the classroom should be added (i.e. it matches the building and its timetable is not empty), false otherwise
        
    # NOTE: Entry with classroom name "Wayne & William White Engineering Design Centre" has an empty timetable, should be skipped
    if building_name == BuildingCode.EDC.name and re.fullmatch(building_name, classroom_name) != None:
        return False
    
    return check_building_match(building_name, classroom_name)



def get_matching_classrooms(driver, building_code : BuildingCode) -> list[str]:
    # For a given classroom type, returns a list of numeric values in string format representing classrooms, where:
    #   - each classroom belongs to the building represented by the building code
    #   - each classroom belongs to the classroom type

    matching_classrooms = []
    all_classrooms = driver.find_elements(By.XPATH, f"//select[@id='{get_classrooms_element_id()}']/option")    # Gets list of all classrooms
    building_name = building_code.value # Gets building name from code

    for classroom in all_classrooms:
        classroom_name = classroom.get_attribute("innerHTML")

        if should_add_classroom(building_name, classroom_name):
            classroom_value = classroom.get_attribute("value")
            matching_classrooms.append(classroom_value)
        
    return matching_classrooms



def get_table_headers() -> list[str]:
    # Return a list of attributes for a classroom booking within an academic year
    # Campus:                   UBCV
    # Year:                     Academic year in format 20XX-XX
    # Building:                 3-5 letter code representing a building
    # Room:                     3-4 digit classroom number
    # RoomType:                 String representing whether the room the booking is in is a general teaching space or a restricted space
    # Capacity:                 Numeric value representing the number of seats in the room
    # Date:                     ISO-8601 compliant date in format YYYY-MM-DD
    # Week:                     Numeric value from 1-(52|53) where 1 represents the first week after the end of the previous academic year's summer session 
    # Day:                      Numeric value from 1-7 where 1 represents Monday, 2 represents Tuesday, ... , 7 represents Sunday
    # Start:                    Time in 24-hour format representing the beginning of a booking
    # End:                      Time in 24-hour format representing the end of a booking
    # Type:                     Code representing the purpose of a booking (e.g. LEC, SEM, LAB)
    # Booking:                  Name of the booking
    # Professor (optional):     Name of the professor associated with the booking
    return ["Campus", "Year", "Building", "Room", "RoomType", "Capacity", "Date", "Week", "Day", "Start", "End", "Type", "Booking", "Professor"]



def scrape_classrooms(driver) -> None:
    # Inserts all bookings for each week as entries in a table, then saves the table as csv

    # Initialize table
    # df = pd.DataFrame(columns=get_table_headers())

    # TODO: implement scraping
    print(driver.page_source) # stub



def scrape(driver, building_code : BuildingCode, classroom_type : ClassroomType) -> None:
    # Parses and saves all classrooms for a given building and classroom type to csv

    # Get chosen timetable options excluding classrooms
    options = get_timetable_options()

    # Sets the chosen timetable options excluding classrooms to be selected
    set_options_selected(driver, options)

    # Gets classroom values matching building code and classroom type
    classrooms = get_matching_classrooms(driver, building_code)

    # set all classrooms as selected
    set_options_selected(driver, {get_classrooms_element_id(): classrooms})

    # click view timetable button
    driver.find_element(By.ID, get_view_timetable_id()).click()

    # navigate to timetable
    driver.get(url + 'showtimetable.aspx')

    # scrape
    scrape_classrooms(driver)

    # return to classrooms page
    driver.get(url)
        


def main() -> None:
    # Scrapes and saves the classroom data to csv

    # TODO: replace with scrape_classrooms_config.json for prod
    configPath = 'config/scrape_classrooms_config_test.json'

    with open(Path(__file__).parent / configPath, encoding='utf8') as f:
        building_code_data = json.load(f)

        # Validate building codes
        for value in building_code_data['buildingCodes']:
            try:
                assert value == BuildingCode[value].value
            except AssertionError:
                print("An invalid building code was entered\n")
                return

        # Navigate to UBC Online Timetable main page
        driver = get_driver()
        driver.get(url)

        # Scrape all classrooms in each building
        for building_code in building_code_data['buildingCodes']:

            # Navigate to general or restricted classrooms page
            for classroom_type in ClassroomType:
                button_id = get_classroom_type_button_id(classroom_type)

                driver.find_element(By.ID, button_id).click()

                # Scrape each classroom belonging to the classroom type and save to csv
                scrape(driver, building_code, classroom_type)



main()


