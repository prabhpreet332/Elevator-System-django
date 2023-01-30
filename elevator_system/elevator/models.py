import uuid

from django.db import models
from model_utils.models import SoftDeletableModel


class Elevator(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    elevator_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem",
        default=None,
        null=False,
        on_delete=models.CASCADE,
    )

    class ElevatorStatusChoices(models.TextChoices):
        BUSY = "Busy"
        AVAILABLE = "Available"
        UNDER_MAINTENANCE = "Under Maintenance"

    class ElevatorDirectionChoices(models.TextChoices):
        UP = "up"
        DOWN = "down"
        STATIONERY = "stationery"

    status = models.CharField(
        choices=ElevatorStatusChoices.choices,
        null=False,
        max_length=50,
        default=ElevatorStatusChoices.AVAILABLE.value,
    )

    @property
    def elevator_direction(self):
        from elevator_admin.models import ElevatorRequest

        request = ElevatorRequest.objects.get(elevator_assigned=self.elevator_id)
        floor_diff = request.destination_floor - request.current_floor
        if floor_diff > 0:
            return self.ElevatorDirectionChoices.UP.value
        elif floor_diff < 0:
            return self.ElevatorDirectionChoices.DOWN.value
        else:
            return self.ElevatorDirectionChoices.STATIONERY.value

    def __str__(self):
        return self.elevator_id


class Floor(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    floor_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem", null=False, on_delete=models.CASCADE
    )
    floor_number = models.IntegerField()

    def __str__(self):
        return self.floor_id
