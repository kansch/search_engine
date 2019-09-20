from django.contrib.gis.db import models


class Camper(models.Model):
    location = models.PointField()
    price_per_day = models.FloatField()
    weekly_discount = models.FloatField(default=0)
