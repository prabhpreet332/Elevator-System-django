from elevator.models import Elevator, Floor
from elevator.serializers import ElevatorSerializer, FloorSerializer
from rest_framework import viewsets


class ElevatorViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorSerializer
    queryset = Elevator.objects.all()


class FloorViewSet(viewsets.ModelViewSet):
    serializer_class = FloorSerializer
    queryset = Floor.objects.all()
