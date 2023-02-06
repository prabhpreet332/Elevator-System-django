# Generated by Django 4.1.5 on 2023-02-06 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elevator", "0005_alter_elevator_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="elevator",
            name="elevator_id",
        ),
        migrations.RemoveField(
            model_name="floor",
            name="floor_id",
        ),
        migrations.AlterField(
            model_name="elevator",
            name="status",
            field=models.CharField(
                choices=[
                    ("busy", "Busy"),
                    ("available", "Available"),
                    ("under_maintenance", "Under Maintenance"),
                ],
                default="available",
                max_length=50,
            ),
        ),
    ]