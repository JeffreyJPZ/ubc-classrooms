"""
Scrapes the classroom schedules from UBC Online Timetable and outputs the raw data in csv format
"""


import re
import pandas as pd
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scripts.models import BuildingCode


url = 'https://sws-van.as.it.ubc.ca/sws_2023/'
campus = "UBCV"

class ClassroomType(Enum):
    # Types of classrooms - 0 is for general teaching spaces that are open to all faculties, 
    #                       1 is for restricted spaces primarily reserved for a respective faculty
    GENERAL = 0
    RESTRICTED = 1


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
        case _:
            print("No matching classroom type was found")
            return ""
    

def get_timetable_options() -> dict:
    # Returns a dictionary with the timetable options mapped to the most comprehensive values
    options = {
                'lbWeeks': '1-53',                                      # Week Range - All Weeks
                'lbDays': '1-7',                                        # Day Range - All Days
                'dlPeriod': '0-10',                                     # Time Range - All Day 07:00-22:00
                'dlType': 'individual;swsurl;UBCSWSLocationIndividual'  # Type of Report - Single (Basic)
            }
    return options


def get_classrooms_element_id() -> str:
    # Returns the id of the element containing the classrooms
    return "dlObject"


def get_view_timetable_id() -> str:
    # Returns the id of the element that enables viewing of a timetable
    return "bGetTimetable"


def set_options_selected(driver, options : dict) -> None:
    # Sets the given timetable options to be selected

    for id in options:
        option = driver.find_element(By.XPATH, f"//select[@id={id}]/option[@selected='selected']")

        # Checks if default selected element's value is not the correct value
        if (option.get_attribute("value") != options[id]):

            # Clears selected element
            driver.execute_script("option.selected = false")

            # Finds correct option and sets it as selected
            option = driver.find_element(By.XPATH, f"//select[@id={id}]/option[@value={options[id]}]")
            driver.execute_script("option.selected = true")
            

def check_building_match(building_name : str, classroom_name : str) -> bool:
    # Returns true if the building name can be found in the classroom name, false otherwise
    # classroom_name is in the format: "[building name] - [room number]"
    
    # Checks for building name in the first part of the classroom name
    return re.match(building_name, classroom_name) != None


def should_add_classroom(building_name : str, classroom_name : str) -> bool:
    # Returns true if the classroom should be added (i.e. it matches the building and its timetable is not empty), false otherwise
        
    # NOTE: Entry with classroom name "Wayne & William White Engineering Design Centre" has an empty timetable, should be skipped
    if building_name == BuildingCode.EDC.name & re.fullmatch(building_name, classroom_name) != None:
        return False
    
    return check_building_match(building_name, classroom_name)


def get_matching_classrooms(driver, building_code : BuildingCode) -> list[str]:
    # For a given classroom type, returns a list of numeric values in string format representing classrooms, where:
    #   - each classroom belongs to the building represented by the building code
    #   - each classroom belongs to the classroom type

    matching_classrooms = []
    all_classrooms = driver.find_elements(By.XPATH, f"//select[@id={get_classrooms_element_id()}]/option")    # Gets list of all classrooms
    building_name = BuildingCode[building_code].value # Gets building name from code

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
    # Date:                     ISO-8601 compliant date in format YYYY-MM-DD
    # Week:                     Numeric value from 1-(52|53) where 1 represents the first week after the end of the previous academic year's summer session 
    # Day:                      Numeric value from 1-7 where 1 represents Monday, 2 represents Tuesday, ... , 7 represents Sunday
    # Start:                    Time in 24-hour format representing the beginning of a booking
    # End:                      Time in 24-hour format representing the end of a booking
    # Type:                     Code representing the purpose of a booking (e.g. LEC, SEM, LAB)
    # Booking:                  Name of the booking
    # Professor (optional):     Name of the professor associated with the booking
    return ["Campus", "Year", "Building", "Room", "Date", "Week", "Day", "Start", "End", "Type", "Booking", "Professor"]


def scrape_classroom(driver) -> None:
    # Inserts all bookings for each week as entries in a table, then saves the table as csv

    # Initialize table
    df = pd.DataFrame(columns=get_table_headers())

    # TODO: implement scraping


def scrape_classrooms(driver, building_code : BuildingCode, classroom_type : ClassroomType) -> None:
    # Parses and saves all classrooms for a given building and classroom type to csv

    # Get chosen timetable options
    options = get_timetable_options()

    # Sets the chosen timetable options to be selected
    set_options_selected(driver, options)

    # Gets classroom values matching building code and classroom type
    classrooms = get_matching_classrooms(driver, building_code)

    # Iterate through each classroom
    for classroom in classrooms:
        # set classroom as selected
        set_options_selected(driver, {get_classrooms_element_id(): classroom})
        # click view timetable button
        driver.find_element(By.ID, get_view_timetable_id()).click()
        # navigate to timetable
        driver.get(url + 'showtimetable.aspx')
        # scrape
        scrape_classroom(driver)
        # return to classrooms page
        driver.get(url)


def main():
    # Scrapes and saves the classroom data to csv

    # Get building code input from user in order to scrape both general and restricted classrooms belonging to building
    input = input("Enter the four letter code of the classrooms to scrape: ")

    try:
        building_code = BuildingCode[input].name
    except ValueError:
        print("An invalid building code was entered\n")
        return

    # Navigate to UBC Online Timetable main page
    driver = get_driver()
    driver.get(url)

    # Navigate to general or restricted classrooms page
    for classroom_type in ClassroomType:
        button_id = get_classroom_type_button_id(classroom_type)

        driver.find_element(By.ID, button_id).click()

        # Scrape each classroom belonging to the classroom type and save to csv
        scrape_classrooms(driver, building_code, classroom_type)



