from rest_framework import viewsets

from .serializers import CamperSerializer
from .models import Camper


class CamperViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CamperSerializer
    queryset = Camper.objects.all()
