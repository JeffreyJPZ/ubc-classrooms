# Manual migration to add building address, latitude and longitude

import json
from pathlib import Path
import django.db.models.deletion
from django.db import migrations, models

from api.utils.ubc import BuildingCodeToFullName
from api.models.building import Building


class Migration(migrations.Migration):
    def update_existing_buildings(apps, schema_editor) -> None:
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

    dependencies = [
        ('api', '0006_remove_building_id_remove_roomtype_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='building_address',
            field=models.CharField(null=True, default=None, db_default=None, max_length=100, help_text="Street address of a UBC building"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='latitude',
            field=models.DecimalField(null=True, default=None, db_default=None, max_digits=8, decimal_places=6, help_text="Latitude data of a UBC building up to 5 significant figures"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='longitude',
            field=models.DecimalField(null=True, default=None, db_default=None, max_digits=9, decimal_places=6, help_text="Longitude data of a UBC building up to 5 significant figures"),
            preserve_default=False,
        ),
        migrations.RunPython(update_existing_buildings),
    ]
