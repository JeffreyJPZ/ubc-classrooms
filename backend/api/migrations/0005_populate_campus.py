# Manual migration

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_create_campus'),
    ]

    operations = [
        migrations.RunSQL("INSERT INTO api_campus (campus_code, campus_name) VALUES ('UBCV', 'Vancouver')"),
        migrations.RunSQL("INSERT INTO api_campus (campus_code, campus_name) VALUES ('UBCO', 'Okanagan')")
    ]
