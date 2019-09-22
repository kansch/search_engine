from django.contrib.gis.db import models


class Camper(models.Model):
    location = models.PointField()
    price_per_day = models.FloatField()
    weekly_discount = models.FloatField(default=0)


class Calendar(models.Model):
    """Contains availabilitites for each Camper."""
    camper = models.ForeignKey(Camper, related_name='calendars', on_delete=models.CASCADE)
    camper_is_available = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
