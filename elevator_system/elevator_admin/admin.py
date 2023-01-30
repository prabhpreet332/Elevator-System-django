from django.contrib import admin

from elevator_admin.models import ElevatorRequest, ElevatorSystem


class ElevatorSystemAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ElevatorSystem._meta.fields]


class ElevatorRequestAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ElevatorRequest._meta.fields]


admin.site.register(ElevatorSystem, ElevatorSystemAdmin)
admin.site.register(ElevatorRequest, ElevatorRequestAdmin)
