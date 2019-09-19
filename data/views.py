import re

from django.contrib.gis.geos import Polygon

from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .serializers import CamperSerializer
from .models import Camper


class CamperViewSet(viewsets.ReadOnlyModelViewSet):

    class CamperFilter(filters.FilterSet):
        location = filters.CharFilter(
            field_name='location',
            method='filter_location',
            label='Location',
            help_text='Campers around this point: lon,lat',
        )

        def filter_location(self, queryset, name, value):
            float_regex = r'[-+]?\d*\.\d+|\d+'
            location_regex = '%s,%s' % (float_regex, float_regex)
            if not re.match(location_regex, value):
                raise ValidationError(detail='location format should be lon,lat')
            coords = value.split(',')
            lon = float(coords[0])
            lat = float(coords[1])
            bbox = (lon - 0.1, lat - 0.1, lon + 0.1, lat + 0.1)
            polygon = Polygon.from_bbox(bbox)
            return queryset.filter(location__contained=polygon)

    serializer_class = CamperSerializer
    queryset = Camper.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CamperFilter
