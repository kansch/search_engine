from django.contrib.gis.geos import Polygon
from django.db.models import F

from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .serializers import CamperSerializer
from .validators import validate_date_range, validate_location
from .models import Camper, Calendar


class CamperViewSet(viewsets.ReadOnlyModelViewSet):

    class CamperFilter(filters.FilterSet):
        location = filters.CharFilter(
            field_name='location',
            method='filter_location',
            label='Location',
            help_text='Campers around this point: lon,lat',
            validators=[validate_location]
        )
        start_date = filters.DateFilter(field_name='calendars__end_date')
        end_date = filters.DateFilter(field_name='calendars__start_date')

        def is_valid(self):
            is_valid = super().is_valid()
            start = self.form.cleaned_data.get('start_date', None)
            end = self.form.cleaned_data.get('end_date', None)
            if is_valid and (start or end):
                validate_date_range(start, end)
            return is_valid

        def filter_queryset(self, queryset):
            """Manage optionals start_date and end_date
            filters and price that depends on it."""
            start = self.form.cleaned_data.pop('start_date', None)
            end = self.form.cleaned_data.pop('end_date', None)
            queryset = super().filter_queryset(queryset)
            # If date are not provided, price returned is the price_per_day.
            days = 1
            if start and end:
                not_available = list(Calendar.objects.filter(
                    start_date__lt=end,
                    end_date__gt=start,
                    camper_is_available=False,
                ).values_list('camper_id', flat=True))

                days = (end - start).days + 1
                queryset = queryset.exclude(id__in=not_available)
            price = days * F('price_per_day')
            # Discount is applied for rentals of 7 days or more.
            if days >= 7:
                price = price * (1 - F('weekly_discount'))
            queryset = queryset.annotate(price=price)
            return queryset

        def filter_location(self, queryset, name, value):
            coords = value.split(',')
            lon, lat = float(coords[0]), float(coords[1])
            bbox = (lon - 0.1, lat - 0.1, lon + 0.1, lat + 0.1)
            polygon = Polygon.from_bbox(bbox)
            return queryset.filter(location__contained=polygon)

    serializer_class = CamperSerializer
    queryset = Camper.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = CamperFilter
    ordering = ['price']
