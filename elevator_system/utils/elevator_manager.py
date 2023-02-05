from django.db.models import Q
from elevator.models import Elevator, ElevatorDirectionChoices, ElevatorStatusChoices
from elevator_admin.models import ElevatorRequest, ElevatorSystem


class ElevatorManager:
    def __init__(self) -> None:

        pass

    # def process_request(self):
    #     self.accept_request()

    def accept_request(
        self, system: ElevatorSystem, elevator_request_obj: ElevatorRequest
    ):
        list_elevators = Elevator.objects.filter(
            ~Q(status=ElevatorStatusChoices.UNDER_MAINTENANCE.value), system=system
        )

        for elevator in list_elevators:
            if elevator.status == ElevatorStatusChoices.AVAILABLE.values:
                # when elevator is done fulfilling other requests and
                # is completely idle at the moment

                requests = (
                    elevator_request_obj.filter(
                        is_resolved=False,
                        system=system,
                    )
                    .order_by("-created")
                    .first()
                )
                # request accepted of the first floor to request an elevator
                requests.update(elevator_assigned=elevator)

            elif elevator.status == ElevatorStatusChoices.BUSY.values:
                # when elevator is already fulfilling some other request

                if elevator.elevator_direction == ElevatorDirectionChoices.UP.value:
                    requests = elevator_request_obj.filter(
                        is_resolved=False,
                        system=system,
                        current_floor_number__gt=elevator.current_floor_number,
                        expected_elevator_direction=ElevatorDirectionChoices.UP.value,
                    ).order_by("current_floor_number")

                    # request accepted
                    requests.update(elevator_assigned=elevator)

                elif elevator.elevator_direction == ElevatorDirectionChoices.DOWN.value:
                    requests = elevator_request_obj.filter(
                        is_resolved=False,
                        system=system,
                        current_floor_number__st=elevator.current_floor_number,
                        expected_elevator_direction=ElevatorDirectionChoices.DOWN.value,
                    ).order_by("-current_floor_number")

                    # request accepted
                    requests.update(elevator_assigned=elevator)
            else:
                # all elevators are under maintenance
                pass
