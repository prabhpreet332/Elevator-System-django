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
        data = super().validate(data)
        errors = {}

        errors.update(self.floor_count_validation(data))
        errors.update(self.elevator_count_validation(data))

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ElevatorSystemOutputSerializer(ElevatorSystemInputSerializer):
    class Meta:
        model = ElevatorSystem
        fields = ["id", "system_id"] + ElevatorSystemInputSerializer.Meta.fields


class ElevatorSystemMaintenanceSerializer(serializers.ModelSerializer):
    elevators = serializers.ListField(
        child=serializers.IntegerField(allow_null=False), allow_empty=False
    )

    class Meta:
        model = ElevatorSystem
        fields = "__all__"

    def validate(self, data):
        data = super().validate(data)
        errors = dict()

        elevators = data["elevators"]

        system_id = self.context["system_id"]
        try:
            system = ElevatorSystem.objects.get(id=system_id)
        except ElevatorSystem.DoesNotExist:
            errors.update({"system_id": "system id does not exists"})
            raise serializers.ValidationError(errors)

        from elevator.models import Elevator

        for elevator_id in elevators:
            if not Elevator.objects.filter(system=system, id=elevator_id).exists():
                errors.update(
                    {f"elevators.id={elevator_id}": "Does not exists for the system"}
                )
        if errors:
            raise serializers.ValidationError(errors)
        return data


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = "__all__"
