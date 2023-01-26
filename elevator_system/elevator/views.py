from rest_framework import viewsets

from elevator.models import Elevator
from elevator.serializers import ElevatorSerializer

class ElevatorView(viewsets.ModelViewSet):
    serializer_class = ElevatorSerializer
    queryset = Elevator.objects.all()
