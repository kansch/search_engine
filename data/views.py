from django.contrib.gis.geos import Polygon
from django.db.models import F

from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .serializers import CamperSerializer
from .validators import validate_date_range, validate_location
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
            lon, lat = validate_location(value)
            bbox = (lon - 0.1, lat - 0.1, lon + 0.1, lat + 0.1)
            polygon = Polygon.from_bbox(bbox)
            return queryset.filter(location__contained=polygon)

    serializer_class = CamperSerializer
    queryset = Camper.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = CamperFilter
    ordering = ['price']

    def get_queryset(self):
        """Manage optionals start_date and end_date
        parameters and price that depends on it."""
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        # If date are not provided, price returned is the price_per_day.
        days = 1
        if start_date or end_date:
            start, end = validate_date_range(start_date, end_date)
            days = (end - start).days + 1

        price = days * F('price_per_day')
        # Discount is applied for rentals of 7 days or more.
        if days >= 7:
            price = price * (1 - F('weekly_discount'))
        queryset = queryset.annotate(price=price)
        return queryset
