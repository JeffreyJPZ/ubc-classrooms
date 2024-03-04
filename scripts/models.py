# Models used throughout scripts


from enum import Enum


# - Most building codes were taken from wiki.ubc.ca
# - If there were conflicting values with UBC Online Timetable, (e.g. abbreviations), 
#   then UBC Online Timetable name was preferred
# - Comments denote whether buildings' classrooms are all restricted and/or other notes
class BuildingCode(Enum):
    # Building codes for UBC names and their full names (with exceptions)
    
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
    CHBE2 = "Chemical and Biological Engineering" # Restricted # Alternative to Chemical and Biological Eng used for one entry
    CHEM = "Chemistry"
    CIRS = "CIRS"
    CEME = "Civil and Mechanical Eng."
    CEMEL = "Civil and Mechanical Eng. Labs" # Restricted
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
    GREN = "Greenhouse(Horticultural Bldg)" # Restricted
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
    JBM = "Macdonald" # Restricted
    MCLD = "MacLeod Building"
    MCLM = "MacMillan"
    MATH = "Mathematics"
    MATX = "Mathematics Annex"
    MBC = "Medical Block C" # Restricted
    MEM = "Memorial Gymnasium" # Restricted
    MSL = "Michael Smith Laboratories" # Restricted
    MUSC = "Music" # Restricted
    SCRF = "Neville Scarfe"
    ORCH = "Orchard Commons"
    OSB2 = "Osborne Centre"
    PHRM = "Pharmaceutical Sciences"
    PONE = "Ponderosa Annex E"
    PCN = "Ponderosa Commons North"
    PCE = "Ponderosa Commons East Audain Art" # Restricted
    RUH = "Ritsumeikan-UBC House" # Restricted
    SPPH = "School Populatn & Publc Hlth" # Restricted
    SING = "Sing Tao School of Journalism" # Restricted
    TFPB = "Theatre-Film Production Building"# Restricted
    TFS = "Totem Field Studios" # Restricted
    UCEN = "Leon & Thea Koerner University Centre"
    LIFE = "UBC Life Building" 
    EDC = "Wayne & William White Engineering Design Centre" # Restricted # One entry is just the building name and has no associated timetable
    WESB = "Wesbrook"
    SWNG = "West Mall Swing Space"
    IRC = "Woodward IRC"
