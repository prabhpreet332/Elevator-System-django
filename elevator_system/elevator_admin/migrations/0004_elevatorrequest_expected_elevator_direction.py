# Generated by Django 4.1.5 on 2023-02-06 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elevator_admin", "0003_alter_elevatorrequest_elevator_assigned"),
    ]

    operations = [
        migrations.AddField(
            model_name="elevatorrequest",
            name="expected_elevator_direction",
            field=models.CharField(
                choices=[("up", "Up"), ("down", "Down"), ("idle", "Idle")],
                default="idle",
                max_length=20,
            ),
        ),
    ]
