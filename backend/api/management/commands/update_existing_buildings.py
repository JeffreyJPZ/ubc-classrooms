import json
from pathlib import Path
from django.core.management.base import BaseCommand

from api.utils.ubc import *
from api.models.building import Building

class Command(BaseCommand):
    help = "Add building address, latitude, and longitude to existing building records"

    def handle(self, *args, **options) -> None:
        # Sets building, latitude and longitude fields for existing buildings using data from building coordinates file

        def is_valid_building(building_name: str) -> bool:
            try:
                return building_name == BuildingCodeToFullName(building_name).value
            except ValueError:
                return False
                
        path = Path.cwd() / 'data' / 'building_coordinates' / 'UBCV' / 'ubcv_building_coordinates.json'

        with open(path, mode="r") as f:
            buildings_data: list[object[str, str or float]] = json.load(f)
            
            # Ignore non-existing buildings
            filtered_buildings_data = filter(lambda building: is_valid_building(building["building_name"]), buildings_data)

            for building in filtered_buildings_data:
                # Building code is primary key
                code = BuildingCodeToFullName(building["building_name"]).name
                Building.objects.filter(building_code=code).update(building_address=building["building_address"], latitude=building["latitude"], longitude=building["longitude"])