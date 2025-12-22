from django.db import models
from recsa_challenge.util.base_model import BaseModel

class Appointment(BaseModel):
    # Usamos CharField para el paciente por simplicidad, 
    # en un sistema real podría ser una FK a un modelo User.
    patient_name = models.CharField("Nombre Paciente", max_length=255)
    date = models.DateField("Fecha")
    time = models.TimeField("Hora")
    reason = models.TextField("Motivo", blank=True, null=True)
    
    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time}"