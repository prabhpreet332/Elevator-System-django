from django.db.models import Q
from elevator.models import Elevator, ElevatorDirectionChoices, ElevatorStatusChoices
from elevator_admin.models import ElevatorRequest, ElevatorSystem


class ElevatorManager:
    def __init__(self, system: ElevatorSystem) -> None:
        self.system = system

    def process_request(self, elevator_request_objs: ElevatorRequest):
        elevators = Elevator.objects.filter(system=self.system, status=ElevatorStatusChoices.BUSY.value)
        for elevator in elevators:
            if elevator_request_objs.count() == 0:
                break
            
            requests = elevator_request_objs.filter(elevator_assigned=elevator, is_resolved=False)
            min_floor, max_floor = int(1e9), -int(1e9)
            for request in requests:
                min_floor = min(min_floor, request.destination_floor_number)
                max_floor = max(max_floor, request.destination_floor_number)
            

            for request in requests:
                # print(request.id)
                if request.expected_elevator_direction == ElevatorDirectionChoices.UP.value:
                    elevator.current_floor_number = max_floor
                elif request.expected_elevator_direction == ElevatorDirectionChoices.DOWN.value:
                    elevator.current_floor_number = min_floor
            elevator.status=ElevatorStatusChoices.AVAILABLE.value
            elevator.direction=ElevatorDirectionChoices.IDLE.value
            elevator.save()
            requests.update(is_resolved=True)

            # up_requests = requests.objects.filter(expected_elevator_direction=ElevatorDirectionChoices.UP.value)

            # for req in up_requests:
            # elevator.current_floor_number = req.destination_floor_number
            # req.elevator_assigned

    #     self.accept_request()
    # def elevator_direction(self, elevator_request_obj: ElevatorRequest):
    #     if elevator_request_obj.elevator_assigned is not None and  elevator_request_obj.destination_floor_number > elevator_request_obj.current_floor_number:
    #         return ElevatorDirectionChoices.UP.value
    #     elif elevator_request_obj.elevator_assigned is not None and  elevator_request_obj.destination_floor_number < elevator_request_obj.current_floor_number:
    #         return ElevatorDirectionChoices.DOWN.value

    def accept_request(self, elevator_request_objs: ElevatorRequest):
        list_elevators = Elevator.objects.filter(
            ~Q(status=ElevatorStatusChoices.UNDER_MAINTENANCE.value), system=self.system
        )

        for elevator in list_elevators:
            if elevator_request_objs.count() == 0:
                break

            if elevator.status == ElevatorStatusChoices.AVAILABLE.value:
                # when elevator is done fulfilling other requests and
                # is completely idle at the moment

                requests = (
                    elevator_request_objs.filter(system=self.system)
                    .order_by("-created")
                    .first()
                )
                # request accepted of the first floor to request an elevator
                requests.elevator_assigned = elevator
                elevator.status = ElevatorStatusChoices.BUSY.value
                elevator.current_floor_number = requests.current_floor_number
                elevator.direction = requests.expected_elevator_direction
                elevator.save()
                requests.save()

            elif elevator.status == ElevatorStatusChoices.BUSY.value:
                # when elevator is already fulfilling some other request

                if elevator.direction == ElevatorDirectionChoices.UP.value:
                    requests = elevator_request_objs.filter(
                        current_floor_number__gte=elevator.current_floor_number,
                        expected_elevator_direction=ElevatorDirectionChoices.UP.value,
                    ).order_by("current_floor_number")
                    
                    # print("==========================")
                    # print(requests.expected_elevator_direction)

                    # request accepted
                    requests.update(elevator_assigned=elevator)
                    elevator.direction = ElevatorDirectionChoices.UP.value
                    elevator.save()


                elif elevator.direction == ElevatorDirectionChoices.DOWN.value:
                    requests = elevator_request_objs.filter(
                        current_floor_number__lte=elevator.current_floor_number,
                        expected_elevator_direction=ElevatorDirectionChoices.DOWN.value,
                    ).order_by("-current_floor_number")

                    # print("==========================")
                    # print(requests.count())
                    # # print(requests.expected_elevator_direction)
                    # print(requests)

                    # request accepted
                    requests.update(elevator_assigned=elevator)
                    elevator.direction = ElevatorDirectionChoices.DOWN.value
                    elevator.save()

