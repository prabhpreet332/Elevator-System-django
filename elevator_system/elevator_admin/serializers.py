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


class ElevatorRequestInputSerializer(serializers.ModelSerializer):
    current_floor_number = serializers.IntegerField(allow_null=False)
    destination_floor_number = serializers.IntegerField(allow_null=False)
    system_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = ElevatorRequest
        fields = ["current_floor_number", "destination_floor_number", "system_id"]

    def system_validate(self, data):
        errors = dict()
        system_id = data["system_id"]
        system_objs = ElevatorSystem.objects.filter(id=system_id)
        if system_objs.count() == 0:
            errors[
                "system.key"
            ] = f"Elevator System with the value: {system_id} does not exist"
            raise serializers.ValidationError(errors)
        return errors

    def floors_validate(self, data):
        errors = dict()

        system_id = data["system_id"]
        system_obj = ElevatorSystem.objects.filter(id=system_id).first()

        current_floor_number = data["current_floor_number"]
        destination_floor_number = data["destination_floor_number"]
        top_floor = system_obj.floor_count - 1

        if not (current_floor_number <= top_floor and current_floor_number >= 0):
            errors[
                "current_floor_number.value"
            ] = f"This value should be between Max Floor: {top_floor} and Min Floor: 0"

        if not (
            destination_floor_number <= top_floor and destination_floor_number >= 0
        ):
            errors[
                "destination_floor_number.value"
            ] = f"This value should be between Max Floor: {top_floor} and Min Floor: 0"
        if  destination_floor_number == current_floor_number:
            errors[
                "current_floor_number.destination_floor_number.value"
            ] = "The values of `current_floor_number` and `destination_floor_number` should be different."

        return errors

    def validate(self, data):
        data = super().validate(data)

        errors = dict()

        errors.update(self.system_validate(data))
        errors.update(self.floors_validate(data))

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ElevatorRequestOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = [
            "id",
            "current_floor_number",
            "destination_floor_number",
            "system",
            "elevator_assigned",
        ]


class ElevatorRequestProcessSerializer(serializers.ModelSerializer):
    system_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = ElevatorRequest
        fields = ["system_id"]

    def system_validate(self, data):
        errors = dict()
        system_id = data["system_id"]
        system_objs = ElevatorSystem.objects.filter(id=system_id)
        if system_objs.count() == 0:
            errors[
                "system.key"
            ] = f"Elevator System with the value: {system_id} does not exist"
            raise serializers.ValidationError(errors)
        return errors

    def validate(self, data):
        data = super().validate(data)

        errors = dict()

        errors.update(self.system_validate(data))

        if errors:
            raise serializers.ValidationError(errors)

        return data
