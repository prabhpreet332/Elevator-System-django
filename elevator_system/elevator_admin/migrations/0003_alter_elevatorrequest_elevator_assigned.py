# Generated by Django 4.1.5 on 2023-02-06 01:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elevator", "0004_elevator_direction"),
        ("elevator_admin", "0002_remove_elevatorsystem_bottommost_floor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="elevatorrequest",
            name="elevator_assigned",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="elevator.elevator",
            ),
        ),
    ]
