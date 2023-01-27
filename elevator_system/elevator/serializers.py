from elevator.models import Elevator
from rest_framework import serializers


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = "__all__"
