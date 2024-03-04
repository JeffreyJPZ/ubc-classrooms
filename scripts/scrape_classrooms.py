"""
Scrapes the classroom schedules from UBC Online Timetable and outputs the raw data in csv format
"""

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


def get_classroom_type_button_id(classroom_type):
    # Returns a string representing the button id for the given classroom type
    match classroom_type:
        case ClassroomType.GENERAL:
            return "LinkBtn_locationByZone"
        case ClassroomType.RESTRICTED:
            return "LinkBtn_locationRestricted"
        case _:
            print("No matching classroom type was found")
            return ""
    

def get_timetable_options():
    # Returns a dictionary with the timetable options mapped to the most comprehensive values
    options = {
                'lbWeeks': '1-53',                                      # Week Range - All Weeks
                'lbDays': '1-7',                                        # Day Range - All Days
                'dlPeriod': '0-10',                                     # Time Range - All Day 07:00-22:00
                'dlType': 'individual;swsurl;UBCSWSLocationIndividual'  # Type of Report - Single (Basic)
            }
    return options


def get_classrooms_element_id():
    # Returns the id of the element containing the classrooms
    return "dlObject"


def set_timetable_options(driver, options):
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
            

def check_building_match(building_name, classroom_name):
    # Returns true if the building name can be found in the classroom name, false otherwise
    # classroom_name is in the format: "[building name] - [room number]"
    # NOTE: First Wayne & William White Engineering Design Centre entry is exception - no dash

    # TODO: use regex matching to implement
    return False # stub



def get_classrooms(driver, building_code, classroom_type):
    # Returns a list of classrooms represented by numeric values, where:
    #   - each classroom belongs to the building represented by the building code
    #   - each classroom belongs to the classroom type

    # TODO: implement by calling get_building_match, 
    #       check for case where classroom name is exactly Wayne & William White Engineering Design Centre and return immediately if so,
    #       otherwise add value attribute of classroom element to list
    classrooms = []

    return classrooms # stub

            
def scrape(driver, building_code, classroom_type):
    # Parses and saves all classrooms for a given type to the appropriate csv for their building

    # Get chosen timetable options
    options = get_timetable_options()

    # Sets the chosen timetable options to be selected
    set_timetable_options(driver, options)

    # TODO call get_classrooms
    

def main():
    # Scrapes and saves the classroom data to csv

    # Navigate to UBC Online Timetable main page
    driver = get_driver()
    driver.get(url)

    # Navigate to general or restricted classrooms page
    # for type in ClassroomType:
    #     button_id = get_classroom_type_button_id(type)

    #     driver.find_element(By.ID, button_id).click()

    #     # Scrape each classroom belonging to the classroom type and save to csv
    #     scrape(driver, type)

    # TODO: get building code input from user in order to scrape both general and restricted classrooms belonging to building

