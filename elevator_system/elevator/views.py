from elevator.models import Elevator
from elevator.serializers import ElevatorSerializer
from rest_framework import viewsets


class ElevatorView(viewsets.ModelViewSet):
    serializer_class = ElevatorSerializer
    queryset = Elevator.objects.all()
