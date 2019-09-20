from rest_framework import serializers

from .models import Camper


class CamperSerializer(serializers.ModelSerializer):

    camper_id = serializers.IntegerField(source='id')
    price = serializers.FloatField()

    class Meta:
        model = Camper
        fields = ('camper_id', 'price')
