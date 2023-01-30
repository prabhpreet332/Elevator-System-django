from elevator_admin.models import ElevatorRequest, ElevatorSystem
from rest_framework import serializers


class ElevatorSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorSystem
        fields = "__all__"


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = "__all__"
