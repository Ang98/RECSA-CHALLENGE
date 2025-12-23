from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from recsa_challenge.chat.service import OpenAIService

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        history = request.data.get('history', []) 
        
        # 2. Obtenemos la fecha y hora actual real
        now = timezone.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        # 3. Definimos el "Cerebro" del bot con reglas estrictas
        system_prompt = f"""
        Eres un asistente médico virtual útil y profesional de RECSA.
        
        INFORMACIÓN DE CONTEXTO:
        - Fecha actual: {current_date}
        - Hora actual: {current_time}
        
        REGLAS CRÍTICAS DE FUNCIONAMIENTO (SÍGUELAS ESTRICTAMENTE):

        1. **NUNCA INVENTES UN ID:** Si el usuario te pide modificar o cancelar una cita y NO te ha dado el ID explícitamente, ESTÁ PROHIBIDO adivinar un número (como 1, 100, etc.).
        
        2. **FLUJO OBLIGATORIO PARA MODIFICAR/ELIMINAR:**
           - Si el usuario dice "cancela la cita de Juan", PRIMERO debes ejecutar la herramienta `get_appointments` filtrando por el nombre "Juan".
           - Analiza la respuesta de esa herramienta para encontrar el `id` real de la cita.
           - SOLO ENTONCES, ejecuta `cancel_appointment` o `update_appointment` usando ese `id` real que encontraste.

        3. **FECHAS RELATIVAS:** Si el usuario dice "mañana", calcula la fecha basándote en que hoy es {current_date}.
        
        4. **RESPUESTAS:** Sé amable, confirma las acciones y si hay error, explícalo claramente.
        """

        # Construimos la lista de mensajes
        messages = [{"role": "system", "content": system_prompt}]
        
        # Agregamos historial previo (limitado a últimos 10 para ahorrar tokens)
        messages.extend(history[-10:])
        
        # Agregamos el mensaje actual
        messages.append({"role": "user", "content": user_message})

        # Llamamos al servicio
        service = OpenAIService()
        bot_response = service.chat(messages)

        return Response({"response": bot_response})