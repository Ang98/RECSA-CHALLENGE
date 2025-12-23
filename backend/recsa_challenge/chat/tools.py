import json
from recsa_challenge.appointments.models import Appointment

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "create_appointment",
            "description": "Agendar una nueva cita. Requiere nombre, fecha y hora.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {"type": "string", "description": "Nombre completo del paciente"},
                    "date": {"type": "string", "description": "Fecha (YYYY-MM-DD)"},
                    "time": {"type": "string", "description": "Hora (HH:MM)"},
                    "reason": {"type": "string", "description": "Motivo (opcional)"}
                },
                "required": ["patient_name", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_appointments",
            "description": "Listar citas. Útil para ver IDs antes de modificar/borrar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {"type": "string", "description": "Filtrar por nombre del paciente (opcional)"},
                    "date": {"type": "string", "description": "Filtrar por fecha YYYY-MM-DD (opcional)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_appointment",
            "description": "Modificar una cita. Si no tienes el ID, intenta dar el nombre del paciente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "description": "ID exacto de la cita (Preferido)"},
                    "patient_name": {"type": "string", "description": "Nombre del paciente (Usar si no se tiene ID)"},
                    "date": {"type": "string", "description": "Nueva fecha YYYY-MM-DD"},
                    "time": {"type": "string", "description": "Nueva hora HH:MM"},
                    "reason": {"type": "string", "description": "Nuevo motivo"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancelar/Eliminar una cita. Preferible usar ID, pero acepta nombre.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "description": "ID de la cita"},
                    "patient_name": {"type": "string", "description": "Nombre del paciente para buscar y borrar"}
                }
            }
        }
    }
]

def _find_appointment(appointment_id=None, patient_name=None):
    """
    Función auxiliar para encontrar una cita ya sea por ID o por Nombre.
    Retorna (instancia, mensaje_error).
    """
    if appointment_id:
        try:
            return Appointment.objects.get(id=appointment_id), None
        except Appointment.DoesNotExist:
            return None, f"Error: No existe ninguna cita con el ID {appointment_id}."

    if patient_name:
        # Buscamos por nombre (insensible a mayúsculas)
        citas = Appointment.objects.filter(patient_name__icontains=patient_name)
        count = citas.count()
        
        if count == 0:
            return None, f"Error: No encontré citas para el paciente '{patient_name}'."
        elif count == 1:
            return citas.first(), None
        else:
            # Si hay muchos con el mismo nombre, pedimos más detalles
            return None, f"Error: Hay {count} citas para '{patient_name}'. Por favor especifica la fecha o usa el ID."

    return None, "Error: Debes proporcionar un ID o un nombre de paciente."


def create_appointment(patient_name, date, time, reason="Consulta General"):
    try:
        cita = Appointment.objects.create(
            patient_name=patient_name, date=date, time=time, reason=reason
        )
        return json.dumps({
            "status": "success",
            "message": f"Cita creada para {patient_name} el {date} a las {time}. (ID: {cita.id})"
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def get_appointments(patient_name=None, date=None):
    citas = Appointment.objects.all()
    
    if patient_name:
        citas = citas.filter(patient_name__icontains=patient_name)
    if date:
        citas = citas.filter(date=date)
        
    if not citas.exists():
        return json.dumps({"status": "info", "message": "No se encontraron citas con esos criterios."})

    data = [
        {
            "id": c.id, 
            "paciente": c.patient_name, 
            "fecha": str(c.date), 
            "hora": str(c.time),
            "motivo": c.reason
        } 
        for c in citas
    ]
    return json.dumps(data)

def update_appointment(appointment_id=None, patient_name=None, date=None, time=None, reason=None):
    # Usamos el helper para encontrar la cita
    cita, error = _find_appointment(appointment_id, patient_name)
    if error:
        return json.dumps({"status": "error", "message": error})

    try:
        if date: cita.date = date
        if time: cita.time = time
        if reason: cita.reason = reason
        cita.save()
        
        return json.dumps({
            "status": "success", 
            "message": f"Cita actualizada correctamente. Nueva fecha: {cita.date} {cita.time}"
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def cancel_appointment(appointment_id=None, patient_name=None):
    # Usamos el helper para encontrar la cita
    cita, error = _find_appointment(appointment_id, patient_name)
    if error:
        return json.dumps({"status": "error", "message": error})
    
    try:
        details = f"{cita.patient_name} el {cita.date}"
        cita.delete()
        return json.dumps({
            "status": "success", 
            "message": f"Cita de {details} eliminada correctamente."
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

AVAILABLE_FUNCTIONS = {
    "create_appointment": create_appointment,
    "get_appointments": get_appointments,
    "update_appointment": update_appointment,
    "cancel_appointment": cancel_appointment
}