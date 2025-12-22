from django.utils import timezone
from recsa_challenge.appointments.models import Appointment
import json

# 1. Definición de las herramientas (Schema para OpenAI)
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "create_appointment",
            "description": "Agendar una nueva cita médica. Solicita siempre fecha (YYYY-MM-DD) y hora (HH:MM).",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {"type": "string", "description": "Nombre del paciente"},
                    "date": {"type": "string", "description": "Fecha en formato YYYY-MM-DD"},
                    "time": {"type": "string", "description": "Hora en formato HH:MM"},
                    "reason": {"type": "string", "description": "Motivo de la consulta"}
                },
                "required": ["patient_name", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_appointments",
            "description": "Listar citas existentes. Puede filtrar por fecha.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Fecha opcional para filtrar (YYYY-MM-DD)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_appointment",
            "description": "Modificar una cita existente (fecha, hora o motivo). Requiere el ID de la cita.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "description": "ID de la cita a modificar"},
                    "date": {"type": "string", "description": "Nueva fecha (YYYY-MM-DD) (opcional)"},
                    "time": {"type": "string", "description": "Nueva hora (HH:MM) (opcional)"},
                    "reason": {"type": "string", "description": "Nuevo motivo (opcional)"}
                },
                "required": ["appointment_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancelar o eliminar una cita médica dado su ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "description": "ID de la cita a eliminar"}
                },
                "required": ["appointment_id"]
            }
        }
    }
]

# 2. Funciones reales (Lógica de Python)
def create_appointment(patient_name, date, time, reason="Consulta General"):
    try:
        cita = Appointment.objects.create(
            patient_name=patient_name,
            date=date,
            time=time,
            reason=reason
        )
        return json.dumps({"status": "success", "id": cita.id, "mensaje": "Cita creada correctamente."})
    except Exception as e:
        return json.dumps({"status": "error", "mensaje": str(e)})

def get_appointments(date=None):
    citas = Appointment.objects.all()
    if date:
        citas = citas.filter(date=date)
    
    # IMPORTANTE: Incluimos el ID para que el bot sepa cuál modificar
    data = [{"id": c.id, "paciente": c.patient_name, "fecha": str(c.date), "hora": str(c.time)} for c in citas]
    return json.dumps(data)

def update_appointment(appointment_id, date=None, time=None, reason=None):
    try:
        cita = Appointment.objects.get(id=appointment_id)
        
        # Solo actualizamos los campos que nos enviaron
        if date:
            cita.date = date
        if time:
            cita.time = time
        if reason:
            cita.reason = reason
            
        cita.save()
        return json.dumps({"status": "success", "mensaje": f"Cita {appointment_id} actualizada correctamente."})
    except Appointment.DoesNotExist:
        return json.dumps({"status": "error", "mensaje": "Cita no encontrada."})
    except Exception as e:
        return json.dumps({"status": "error", "mensaje": str(e)})

def cancel_appointment(appointment_id):
    try:
        cita = Appointment.objects.get(id=appointment_id)
        cita.delete()
        return json.dumps({"status": "success", "mensaje": f"Cita {appointment_id} eliminada."})
    except Appointment.DoesNotExist:
        return json.dumps({"status": "error", "mensaje": "Cita no encontrada."})

# Diccionario para mapear nombres a funciones
AVAILABLE_FUNCTIONS = {
    "create_appointment": create_appointment,
    "get_appointments": get_appointments,
    "update_appointment": update_appointment,
    "cancel_appointment": cancel_appointment
}