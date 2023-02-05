from elevator_admin.models import ElevatorRequest, ElevatorSystem
from rest_framework import serializers


class ElevatorSystemInputSerializer(serializers.ModelSerializer):
    floor_count = serializers.IntegerField(allow_null=False)
    elevator_count = serializers.IntegerField(allow_null=False)

    class Meta:
        model = ElevatorSystem
        fields = ["floor_count", "elevator_count"]

    def floor_count_validation(self, data):
        errors = {}
        floor_count = data["floor_count"]
        if floor_count <= 1:
            errors["floor_count.value"] = "floor_count should be atleast 2"

        return errors

    def elevator_count_validation(self, data):
        errors = {}
        elevator_count = data["elevator_count"]

        if elevator_count <= 0:
            errors["elevator_count.value"] = "elevator_count should be atleast 1"

        return errors

    def validate(self, data):
        errors = {}

        errors.update(self.floor_count_validation(data))
        errors.update(self.elevator_count_validation(data))

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)


class ElevatorSystemOutputSerializer(ElevatorSystemInputSerializer):
    class Meta:
        model = ElevatorSystem
        fields = ["id", "system_id"] + ElevatorSystemInputSerializer.Meta.fields


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = "__all__"
