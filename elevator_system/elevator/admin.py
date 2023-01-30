from django.contrib import admin
from elevator.models import Elevator, Floor


class ElevatorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Elevator._meta.fields]


class FloorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Floor._meta.fields]


admin.site.register(Elevator, ElevatorAdmin)
admin.site.register(Floor, FloorAdmin)
