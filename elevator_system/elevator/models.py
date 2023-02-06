from django.db import models
from model_utils.models import SoftDeletableModel


class ElevatorStatusChoices(models.TextChoices):
    BUSY = "busy"
    AVAILABLE = "available"
    UNDER_MAINTENANCE = "under_maintenance"


class ElevatorDirectionChoices(models.TextChoices):
    UP = "up"
    DOWN = "down"
    IDLE = "idle"


class ElevatorDoorChoices(models.TextChoices):
    OPEN = "open"
    CLOSE = "close"


class Elevator(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
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

    direction = models.CharField(
        choices=ElevatorDirectionChoices.choices,
        null=False,
        max_length=20,
        default=ElevatorDirectionChoices.IDLE.value,
    )

    def __str__(self):
        return str(self.id)


class Floor(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem",
        null=False,
        on_delete=models.CASCADE,
    )
    floor_number = models.IntegerField()

    def __str__(self):
        return str(self.id)
