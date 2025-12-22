from django.contrib import admin
from recsa_challenge.appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Campos visibles en la lista
    list_display = (
        "patient_name",
        "date",
        "time",
        "reason",
        "created",
    )

    # Filtros laterales
    list_filter = (
        "date",
    )

    # Búsqueda
    search_fields = (
        "patient_name",
        "reason",
    )

    # Orden por defecto
    ordering = ("-date", "-time")

    # Campos solo lectura (asumiendo BaseModel)
    readonly_fields = (
        "created",
        "modified",
    )

    # Organización del formulario
    fieldsets = (
        ("Información del paciente", {
            "fields": ("patient_name",),
        }),
        ("Cita", {
            "fields": ("date", "time", "reason"),
        }),
        ("Auditoría", {
            "fields": ("created", "modified"),
        }),
    )
