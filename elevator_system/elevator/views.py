from django_filters.rest_framework import DjangoFilterBackend
from elevator.models import Elevator, ElevatorDoorChoices, ElevatorStatusChoices, Floor
from elevator.serializers import ElevatorSerializer, FloorSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ElevatorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ElevatorSerializer
    queryset = Elevator.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "system",
        "status",
        "door_status",
        "direction",
        "current_floor_number",
    ]

    @action(detail=True, methods=["get"], url_path="status")
    def get_elevator_status(self, request, pk, *args, **kwargs):
        elevator_id = pk
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response(
                {"message": "Elevator ID not Found"}, status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": f"Elevator status extracted for the elevator {elevator.id}",
                "status": elevator.status,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="door-toggle")
    def toggle_doors(self, request, pk, *args, **kwargs):

        elevator_id = pk

        try:
            Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response(
                {"message": "Elevator ID not Found"}, status=status.HTTP_200_OK
            )
        elevator = Elevator.objects.filter(id=elevator_id).first()

        prev_door_status = elevator.door_status
        if elevator.status == ElevatorStatusChoices.AVAILABLE.value:
            if elevator.door_status == ElevatorDoorChoices.CLOSE.value:
                elevator.door_status = ElevatorDoorChoices.OPEN.value
                elevator.status = ElevatorStatusChoices.BUSY.value
                elevator.save()

            else:
                elevator.door_status = ElevatorDoorChoices.CLOSE.value
                elevator.status = ElevatorStatusChoices.AVAILABLE.value
                elevator.save()

        elif (
            elevator.status == ElevatorStatusChoices.BUSY.value
            and elevator.door_status == ElevatorDoorChoices.OPEN.value
        ):
            elevator.door_status = ElevatorDoorChoices.CLOSE.value
            elevator.status = ElevatorStatusChoices.AVAILABLE.value
            elevator.save()

        else:
            return Response(
                {
                    "message": f"Elevator Door Cannot be toggled for the elevator {elevator.id}",
                    "elevator_status": elevator.status,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": f"Elevator Door status Updated for the elevator {elevator.id}",
                "new_door_status": elevator.door_status,
                "previous_door_status": prev_door_status,
                "elevator_status": elevator.status,
            },
            status=status.HTTP_200_OK,
        )


class FloorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FloorSerializer
    queryset = Floor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["system", "floor_number"]
