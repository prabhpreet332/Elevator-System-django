import uuid

from django.db import models
from django.db.models import Q
from django_extensions.db.models import TimeStampedModel
from elevator.models import Elevator
from model_utils.models import SoftDeletableModel


class ElevatorSystem(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    system_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)

    floor_count = models.IntegerField(null=True, default=0)
    elevator_count = models.IntegerField(null=True, default=0)

    bottommost_floor = models.IntegerField(null=True)
    topmost_floor = models.IntegerField(null=True)

    @property
    def is_operating(self):
        idle_elevators_count = (
            Elevator.objects.filter(system=self.system_id)
            .exclude(Q(status=Elevator.ElevatorStatusChoices.AVAILABLE.value))
            .count()
        )
        total_elevators_count = Elevator.objects.filter(system=self.system_id)

        if total_elevators_count == idle_elevators_count:
            return False

        return True

    def __str__(self):
        return self.system_id


class ElevatorRequest(TimeStampedModel, SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    request_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem", null=False, on_delete=models.CASCADE
    )
    elevator_assigned = models.ForeignKey(
        to="elevator.Elevator", default=None, null=True, on_delete=models.CASCADE
    )
    current_floor = models.IntegerField(null=False)
    destination_floor = models.IntegerField(null=False)

    is_resolved = models.BooleanField(default=False, null=False)

    @property
    def is_elevator_assigned(self):
        return self.elevator_assigned is not None

    def __str__(self):
        return self.request_id
