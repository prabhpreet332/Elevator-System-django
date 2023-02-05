import uuid

from django.db import models
from model_utils.models import SoftDeletableModel


class ElevatorStatusChoices(models.TextChoices):
    BUSY = "Busy"
    AVAILABLE = "Available"
    UNDER_MAINTENANCE = "Under Maintenance"


class ElevatorDirectionChoices(models.TextChoices):
    UP = "up"
    DOWN = "down"


class ElevatorDoorChoices(models.TextChoices):
    OPEN = "open"
    CLOSE = "close"


class Elevator(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    elevator_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem",
        default=None,
        null=False,
        on_delete=models.CASCADE,
    )

    current_floor_number = models.IntegerField(default=None)

    status = models.CharField(
        choices=ElevatorStatusChoices.choices,
        null=False,
        max_length=50,
        default=ElevatorStatusChoices.AVAILABLE.value,
    )

    door_status = models.CharField(
        choices=ElevatorDoorChoices.choices,
        null=False,
        max_length=20,
        default=ElevatorDoorChoices.CLOSE.value,
    )

    @property
    def elevator_direction(self):
        from elevator_admin.models import ElevatorRequest

        request = ElevatorRequest.objects.filter(elevator_assigned=self.elevator_id)
        if request.count() == 0:
            self.status = ElevatorStatusChoices.AVAILABLE.value
            return

        request = request.first()
        floor_diff = request.destination_floor_number - request.current_floor_number
        if floor_diff > 0:
            return self.ElevatorDirectionChoices.UP.value
        elif floor_diff < 0:
            return self.ElevatorDirectionChoices.DOWN.value

    def __str__(self):
        return str(self.id)


class Floor(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    floor_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem",
        null=False,
        on_delete=models.CASCADE,
    )
    floor_number = models.IntegerField()

    def __str__(self):
        return str(self.id)
