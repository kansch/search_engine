"""Contains validators for API filters."""
import re
from datetime import datetime

from rest_framework.exceptions import ValidationError


def validate_date_range(start_date, end_date):
    if not (start_date and end_date):
        raise ValidationError(detail='You should provide both start_date and end_date')
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValidationError(detail='Date format should be YYYY-MM-DD')
    if end_date < start_date:
        raise ValidationError(detail='end_date shoud be greater than start_date')
    return start_date, end_date


def validate_location(value):
    float_regex = r'[-+]?\d*\.\d+|\d+'
    location_regex = '%s,%s' % (float_regex, float_regex)
    if not re.match(location_regex, value):
        raise ValidationError(detail='location format should be lon,lat')
    coords = value.split(',')
    return float(coords[0]), float(coords[1])
