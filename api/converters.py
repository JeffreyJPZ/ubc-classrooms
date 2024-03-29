"""
Custom path converters for timeslots API
"""
from datetime import datetime
    
class DateConverter():
    # Matches datestrings in the given format and converts them into dates
    # Credit to https://stackoverflow.com/a/70768674

    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
    format = "%Y-%m-%d"                             # ISO-8601

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()
    
    def to_url(self, value):
        return datetime.strftime(self.format)
        