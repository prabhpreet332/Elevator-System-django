import uuid

from elevator_admin.models import ElevatorRequest, ElevatorSystem
from elevator_admin.serializers import (
    ElevatorRequestSerializer,
    ElevatorSystemInputSerializer,
    ElevatorSystemOutputSerializer,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from utils import utils


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

    # @action()
    # post -- mark elevator as under maintenance
    #       -- if elevator is in maintenance - unmark the requests that elevator accepted as false
    @action(detail=True, methods=["post"], url_path="mark-maintenance")
    def mark_for_maintenance(self, request, pk=None, *args, **kwargs):
        data = request.data
        system_id = pk
        try:
            elevator_system = ElevatorSystem.objects.get(id=system_id)
        except ElevatorSystem.DoesNotExist:
            return Response(
                {"message": "System ID not Found"}, status=status.HTTP_200_OK
            )

        from elevator.models import Elevator

        elevator_for_maintenance = Elevator.objects.filter(
            system=elevator_system, id__in=data["elevators"]
        )
        if elevator_for_maintenance.count() == 0:
            return Response(
                {"message": "Add valid elevator_ids in a list or system ID."},
                status=status.HTTP_200_OK,
            )

        utils.mark_elevator_for_maintenance(elevator_for_maintenance)
        return Response(
            {
                "message": "Elevator status updated to Under-Maintenance.",
            },
            status=status.HTTP_200_OK,
        )


class ElevatorRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorRequestSerializer
    queryset = ElevatorRequest.objects.all()

    # post -- create
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)

    # process api
    @action(detail=True, methods=["post"], url_path="process-request")
    def process_request(self, request, pk=None, *args, **kwargs):
        pass
