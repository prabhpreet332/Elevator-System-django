# Generated by Django 4.1.5 on 2023-02-05 13:17

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Elevator",
            fields=[
                ("is_removed", models.BooleanField(default=False)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("elevator_id", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("current_floor_number", models.IntegerField(default=None)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Busy", "Busy"),
                            ("Available", "Available"),
                            ("Under Maintenance", "Under Maintenance"),
                        ],
                        default="Available",
                        max_length=50,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Floor",
            fields=[
                ("is_removed", models.BooleanField(default=False)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("floor_id", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("floor_number", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
