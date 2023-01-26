from django.db import models


class Elevator(models.Model):
    id = models.AutoField(primary_key=True)
    elevator_id = models.UUIDField()

    def __str__(self):
        return self.elevator_id
