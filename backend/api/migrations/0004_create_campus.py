# Manual migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_building_campus_alter_roomtype_campus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('campus_code', models.CharField(primary_key=True, max_length=4, help_text="UBC campus code")),
                ('campus_name', models.CharField(unique=True, null=False, max_length=20, help_text="UBC campus city name")),
            ],
        )
    ]
