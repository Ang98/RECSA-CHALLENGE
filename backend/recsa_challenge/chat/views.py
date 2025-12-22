from rest_framework.views import APIView
from rest_framework.response import Response
from .service import OpenAIService

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        history = request.data.get('history', []) # Historial previo del frontend
        
        # Construimos el formato de mensajes para OpenAI
        # System prompt: Define la personalidad
        messages = [{"role": "system", "content": "Eres un asistente médico útil de RECSA. Ayudas a agendar, consultar y cancelar citas."}]
        
        # Agregamos historial previo (limitado a últimos 10 mensajes para no gastar tokens)
        messages.extend(history[-10:])
        
        # Agregamos el mensaje actual
        messages.append({"role": "user", "content": user_message})

        # Llamamos al servicio
        service = OpenAIService()
        bot_response = service.chat(messages)

        return Response({"response": bot_response})