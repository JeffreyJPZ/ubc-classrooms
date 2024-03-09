"""
Scrapes the classroom schedules from UBC Online Timetable and outputs the raw data in csv format
"""


import re
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scripts.models import BuildingCode


url = 'https://sws-van.as.it.ubc.ca/sws_2023/'


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


def set_timetable_options(driver, options : dict) -> None:
    # Sets each timetable option's selected element

    for id in options:
        option = driver.find_element(By.XPATH, f"//select[@id={id}]/option[@selected='selected']")

        # Checks if default selected element's value is not the most comprehensive value
        if (option.get_attribute("value") != options[id]):

            # Clears selected element
            driver.execute_script("option.selected = false")

            # Finds most comprehensive option and sets it as selected
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


def get_matching_classrooms(driver, building_code : BuildingCode, classroom_type : ClassroomType) -> list[str]:
    # Returns a list of numeric values in string format representing classrooms, where:
    #   - each classroom belongs to the building represented by the building code
    #   - each classroom belongs to the classroom type

    # TODO: implement by calling get_building_match
    #       otherwise add value attribute of classroom element to list
    matching_classrooms = []
    all_classrooms = driver.find_elements(By.XPATH, f"//select[@id={get_classrooms_element_id()}]/option")    # Gets list of all classrooms
    building_name = BuildingCode[building_code].value # Gets building name from code

    for classroom in all_classrooms:
        classroom_name = classroom.get_attribute("innerHTML")

        if should_add_classroom(building_name, classroom_name):
            classroom_value = classroom.get_attribute("value")
            matching_classrooms.append(classroom_value)
        
    return matching_classrooms

            
def scrape(driver, building_code : BuildingCode, classroom_type : ClassroomType) -> None:
    # Parses and saves all classrooms for a given building and classroom type to csv

    # Get chosen timetable options
    options = get_timetable_options()

    # Sets the chosen timetable options to be selected
    set_timetable_options(driver, options)

    # Gets classrooms matching building code and classroom type
    classrooms = get_matching_classrooms(driver, building_code, classroom_type)
    

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
        scrape(driver, building_code, classroom_type)



