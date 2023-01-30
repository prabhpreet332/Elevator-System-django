from rest_framework import serializers

from elevator_admin.models import ElevatorRequest, ElevatorSystem


class ElevatorSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorSystem
        fields = "__all__"


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = "__all__"
