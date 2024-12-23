"""
Constants for scraping UBC Online Timetable
"""
from enum import Enum
from datetime import datetime, timedelta
from utils.ubc import CampusEnum

class TimetableSettings():
    # UBC Online Timetable information

    CAMPUS = CampusEnum.UBCV.name                               
    ACADEMIC_YEAR = "2024-2025"                             # Change academic year for updated timetable
    URL = 'https://sws-van.as.it.ubc.ca/sws_2024/'          # Change date to get updated timetable
    START_TIME = "07:00"                                    # Earliest time provided by the timetable in 24-hour format
    END_TIME = "22:00"                                      # Latest time provided by the timetable in 24-hour format

    # Reference date for timetable in ISO-8601 format (used in conjunction with week numbers to calculate dates)
    REFERENCE_DATE = "2024-08-19"

    # Calculate start and end dates for scraping
    _now = datetime.now()
    _start = _now - timedelta(days=_now.weekday())
    _end = _start + timedelta(weeks=1, days=6)

    # Describe how to format and parse dates and datetimes
    FORMAT_DATE = "%Y-%m-%d"
    FORMAT_DATETIME = "%Y-%m-%d %H:%M"

    START_DATE = _start.strftime(FORMAT_DATE)                # First day in the chosen time period in ISO-8601 format (date of the current Monday of the week)
    END_DATE = _end.strftime(FORMAT_DATE)                    # Last day in the chosen time period in ISO-8601 format (date of the Sunday of the next week)



# - Most building codes were taken from wiki.ubc.ca
# - If there were conflicting values with UBC Online Timetable, (e.g. abbreviations), 
#   then UBC Online Timetable name was preferred
# - Comments denote whether buildings' classrooms are all restricted and/or other notes
class BuildingCodeToTimetableName(Enum):
    # Building codes for UBC buildings and their names as displayed in UBC Online Timetable
    
    ALRD = "Allard Hall"
    ANSO = "Anthropology and Sociology"
    AERL = "Aquatic Ecosystems Resrch Lab"
    ACEN = "Asian Centre" # Restricted
    AUD = "Auditorium" # Restricted
    AUDX = "Auditorium Annex"
    BINN = "B.C. Binnings Studio" # Restricted
    BIOL = "Biological Sciences"
    BUCH = "Buchanan"
    BUTO = "Buchanan Tower"
    CBH = "Centre for Brain Health" # Restricted
    CHAN = "Chan Ctr Performing Arts" # Restricted
    CHBE = "Chemical and Biological Eng" # Restricted
    CHEM = "Chemistry"
    CIRS = "CIRS"
    CEME = "Civil and Mechanical Eng."
    CEML = "Civil and Mechanical Eng. Labs" # Restricted
    CHOI = "CK Choi" # Restricted
    MINL = "Coal and Mineral Processing" # Restricted
    DLAM = "David Lam Building" # Restricted
    DETW = "Detwiller Pavilion" # Restricted
    DSOM = "Dorothy Somerset Studio" # Restricted
    KENN = "Douglas Kenny" # Restricted
    EOS = "Earth and Ocean Sciences"
    ESB = "Earth Sciences"
    FNH = "Food, Nutrition and Health"
    FSC = "Forest Sciences Centre"
    FORW = "Frank Forward"
    KAIS = "Fred Kaiser" # Restricted
    FRWO = "Frederic Wood Theatre" # Restricted
    FRDM = "Friedman"
    HORT = "Greenhouse(Horticultural Bldg)" # Restricted
    GEOG = "Geography"
    HEBB = "Hebb"
    HENN = "Hennings"
    ANGU = "Henry Angus"
    ICCS = "ICCS" # Restricted
    DMP = "Hugh Dempster Pavilion"
    IONA = "Iona"
    IKB = "Irving K. Barber Learning Ctr"
    KOER = "Koerner Pavilion" # Restricted
    LAX = "Landscape Architecture Annex" # Restricted
    LASR = "Lasserre" # Restricted
    LSK = "Leonard S Klinck" 
    LSC = "Life Sciences Centre" # Restricted
    LIU = "Liu Institute" # Restricted
    LMRS = "Lower Mall Research Station" # Restricted
    MCDN = "Macdonald" # Restricted
    MCLD = "MacLeod Building"
    MCLM = "MacMillan"
    MATH = "Mathematics"
    MATX = "Mathematics Annex"
    MEDC = "Medical Block C" # Restricted
    MGYM = "Memorial Gymnasium" # Restricted
    MSL = "Michael Smith Laboratories" # Restricted
    MUSC = "Music" # Restricted
    SCRF = "Neville Scarfe"
    ORCH = "Orchard Commons"
    OSB2 = "Osborne Centre"
    PHRM = "Pharmaceutical Sciences"
    PONE = "Ponderosa Annex E"
    PCN = "Ponderosa Commons North"
    PCE = "Ponderosa Commons East Audain Art" # Restricted
    RITS = "Ritsumeikan-UBC House" # Restricted
    SPPH = "School Populatn & Publc Hlth" # Restricted
    STAO = "Sing Tao School of Journalism" # Restricted
    TFPB = "Theatre-Film Production Building"# Restricted
    TFS = "Totem Field Studios" # Restricted
    UCEN = "Leon & Thea Koerner University Centre"
    LIFE = "UBC Life Building" 
    EDC = "Wayne & William White Engineering Design Centre" # Restricted # One entry is just the building name and has no associated timetable
    WESB = "Wesbrook"
    SWNG = "West Mall Swing Space"
    IRC = "Woodward IRC"