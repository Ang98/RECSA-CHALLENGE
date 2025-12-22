from rest_framework import viewsets
from recsa_challenge.appointments.models import Appointment
from recsa_challenge.appointments.api.serializers.appoiment_serializer import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # Aquí podríamos agregar permisos o filtros más adelante