# Generated by Django 4.1.5 on 2023-02-06 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elevator_admin", "0004_elevatorrequest_expected_elevator_direction"),
    ]

    operations = [
        migrations.AddField(
            model_name="elevatorrequest",
            name="is_resolved",
            field=models.BooleanField(default=False),
        ),
    ]