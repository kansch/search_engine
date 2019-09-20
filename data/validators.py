"""Contains validators for API filters."""
import re

from rest_framework.exceptions import ValidationError


def validate_date_range(start_date, end_date):
    if not (start_date and end_date):
        raise ValidationError({
            'date_range': ['You should provide both start_date and end_date']
        })

    if end_date < start_date:
        raise ValidationError({
            'end_date': ['end_date shoud be greater than start_date']
        })


def validate_location(value):
    float_regex = r'[-+]?\d*\.\d+|\d+'
    location_regex = '(%s),(%s)' % (float_regex, float_regex)
    if not re.match(location_regex, value):
        raise ValidationError({
            'location': ['Format should be lon,lat']
        })
