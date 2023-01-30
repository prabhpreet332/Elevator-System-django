from elevator_admin.models import ElevatorRequest, ElevatorSystem
from elevator_admin.serializers import (
    ElevatorRequestSerializer,
    ElevatorSystemSerializer,
)
from rest_framework import viewsets


class ElevatorSystemViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorSystemSerializer
    queryset = ElevatorSystem.objects.all()


class ElevatorRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorRequestSerializer
    queryset = ElevatorRequest.objects.all()
