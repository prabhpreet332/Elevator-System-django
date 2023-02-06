import uuid

from elevator.models import ElevatorStatusChoices
from elevator_admin.models import ElevatorRequest, ElevatorSystem
from elevator_admin.serializers import (
    ElevatorRequestInputSerializer,
    ElevatorRequestOutputSerializer,
    ElevatorRequestProcessSerializer,
    ElevatorSystemInputSerializer,
    ElevatorSystemMaintenanceSerializer,
    ElevatorSystemOutputSerializer,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from utils import elevator_manager, utils


class ElevatorSystemViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorSystemOutputSerializer
    queryset = ElevatorSystem.objects.all()

    @action(detail=False, methods=["post"], url_path="initialize")
    def initialize(self, request, *args, **kwargs):
        data = request.data
        serializer = ElevatorSystemInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        system_data = serializer.validated_data

        system_id = uuid.uuid4()
        system_data.update({"system_id": system_id})
        elevator_system = ElevatorSystem.objects.create(**system_data)

        initialized_system_data = utils.initialize_elevators_floors(elevator_system)
        from elevator.models import Elevator, Floor

        system_data.update(
            {
                "id": elevator_system.id,
                "elevator_ids": [
                    str(elevator)
                    for elevator in Elevator.objects.filter(system=elevator_system)
                ],
                "floor_ids": [
                    str(floor) for floor in Floor.objects.filter(system=elevator_system)
                ],
            }
        )
        return Response(
            {"message": initialized_system_data["message"], "system_data": system_data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="mark-maintenance")
    def mark_for_maintenance(self, request, pk=None, *args, **kwargs):
        system_id = pk

        serializer = ElevatorSystemMaintenanceSerializer(
            data=request.data, context={"system_id": system_id}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        from elevator.models import Elevator

        elevator_system = ElevatorSystem.objects.get(id=system_id)

        elevator_for_maintenance = Elevator.objects.filter(
            system=elevator_system, id__in=data["elevators"]
        )
        if elevator_for_maintenance.count() == 0:
            return Response(
                {"message": "Add valid elevator_ids in a list or system ID."},
                status=status.HTTP_200_OK,
            )

        elevator_for_maintenance.filter(
            status=ElevatorStatusChoices.AVAILABLE.value
        ).update(**{"status": ElevatorStatusChoices.UNDER_MAINTENANCE.value})

        return Response(
            {
                "message": "Elevator status updated to Under-Maintenance.",
            },
            status=status.HTTP_200_OK,
        )


class ElevatorRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorRequestOutputSerializer
    queryset = ElevatorRequest.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ElevatorRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        system_id = data["system_id"]
        system_obj = ElevatorSystem.objects.get(id=system_id)

        request_values = {
            "current_floor_number": data["current_floor_number"],
            "destination_floor_number": data["destination_floor_number"],
            "system": system_obj,
        }
        ElevatorRequest.objects.create(**request_values)

        return Response(
            {"message": "Created a request.", "data": data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="accept-request")
    def accept_request(self, request, pk=None, *args, **kwargs):
        serializer = ElevatorRequestProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        system_id = data["system_id"]
        system_obj = ElevatorSystem.objects.get(id=system_id)

        manager = elevator_manager.ElevatorManager(system_obj)
        elevator_request_obj = ElevatorRequest.objects.filter(
            elevator_assigned=None,
            system=system_obj,
        )
        manager.accept_request(elevator_request_obj)
        return Response(
            {"message": "Created a request.", "data": data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="process-request")
    def process_request(self, request, pk=None, *args, **kwargs):
        serializer = ElevatorRequestProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        system_id = data["system_id"]
        system_obj = ElevatorSystem.objects.get(id=system_id)

        manager = elevator_manager.ElevatorManager(system_obj)
        elevator_request_obj = ElevatorRequest.objects.filter(
            system=system_obj,
        )
        manager.process_request(elevator_request_obj)
        return Response(
            {"message": "Created a request.", "data": data},
            status=status.HTTP_200_OK,
        )
