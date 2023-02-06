import uuid

from django.db import models
from django.db.models import Q
from django_extensions.db.models import TimeStampedModel
from elevator.models import Elevator, ElevatorStatusChoices
from model_utils.models import SoftDeletableModel


class ElevatorSystem(SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    system_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)

    floor_count = models.IntegerField(null=True, default=0)
    elevator_count = models.IntegerField(null=True, default=0)

    @property
    def is_operating(self):
        idle_elevators_count = (
            Elevator.objects.filter(system=self.system_id)
            .exclude(Q(status=ElevatorStatusChoices.AVAILABLE.value))
            .count()
        )
        total_elevators_count = Elevator.objects.filter(system=self.system_id)

        if total_elevators_count == idle_elevators_count:
            return False

        return True

    def __str__(self):
        return str(self.id)

    def delete(self, using=None, soft=True, *args, **kwargs):
        # if all elevators are available? (later on)
        # else error
        from elevator.models import Elevator, Floor

        Elevator.objects.filter(system=self.id).delete()
        Floor.objects.filter(system=self.id).delete()

        return super().delete(using, soft, *args, **kwargs)


class ElevatorRequest(TimeStampedModel, SoftDeletableModel):
    id = models.AutoField(primary_key=True)
    request_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4)
    system = models.ForeignKey(
        to="elevator_admin.ElevatorSystem",
        null=False,
        on_delete=models.CASCADE,
    )
    elevator_assigned = models.ForeignKey(
        to="elevator.Elevator",
        default=None,
        null=True,
        on_delete=models.CASCADE,
    )
    current_floor_number = models.IntegerField(null=False)
    destination_floor_number = models.IntegerField(null=False)

    @property
    def is_resolved(self):
        return self.elevator_assigned is not None

    @property
    def expected_elevator_direction(self):
        from elevator.models import ElevatorDirectionChoices

        floor_diff = self.destination_floor_number - self.current_floor_number
        if floor_diff > 0:
            return ElevatorDirectionChoices.UP.value
        elif floor_diff < 0:
            return ElevatorDirectionChoices.DOWN.value

    def __str__(self):
        return str(self.id)
