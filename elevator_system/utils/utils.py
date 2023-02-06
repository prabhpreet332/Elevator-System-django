from django.db import IntegrityError, transaction
from elevator.models import Elevator, Floor


def initialize_elevators_floors(system):
    """Creates the elevator, floor objects in DB during initialization phase.

    Args:
        system: ElevatorSystem - Model Object

    Returns:
        data: dict - contains the elevators, floors created.
    """

    floor_count = system.floor_count
    elevator_count = system.elevator_count
    data = {
        "elevators": None,
        "floors": None,
        "message": "System with the elevators and floors created",
    }
    try:
        with transaction.atomic():
            elevators = list()
            for _ in range(elevator_count):
                elevator = Elevator.objects.create(
                    system=system, current_floor_number=0
                )
                elevators.append(elevator)

            floors = list()
            for floor_number in range(floor_count):
                floor = Floor.objects.create(system=system, floor_number=floor_number)
                floors.append(floor)

            data["elevators"] = tuple(elevators)
            data["floors"] = tuple(floors)

    except IntegrityError as err:
        data["message"] = str(err)

    return data
