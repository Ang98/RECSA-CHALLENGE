
import openai
from django.conf import settings
from recsa_challenge.chat.tools import TOOLS_SCHEMA, AVAILABLE_FUNCTIONS
import json

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    def chat(self, messages):
        """
        Maneja el flujo completo: Usuario -> OpenAI -> (Tool Call?) -> Ejecutar Tool -> OpenAI -> Respuesta Final
        """
        # 1. Primera llamada a OpenAI con el mensaje del usuario y las herramientas disponibles
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto"  # Deja que el modelo decida si usa herramientas
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 2. Si OpenAI quiere llamar a una herramienta...
        if tool_calls:
            # Agregamos el mensaje del asistente al historial (para mantener contexto)
            messages.append(response_message)

            # Iteramos sobre las herramientas que el modelo pidió ejecutar
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🤖 Ejecutando Tool: {function_name} con {function_args}")
                
                function_to_call = AVAILABLE_FUNCTIONS.get(function_name)
                
                if function_to_call:
                    # Ejecutamos la función real de Python (DB)
                    function_response = function_to_call(**function_args)
                    
                    # Agregamos el resultado al historial como mensaje de tipo 'tool'
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })

            # 3. Segunda llamada a OpenAI para que genere la respuesta final en lenguaje natural
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return second_response.choices[0].message.content
        
        # Si no hubo tools, devolvemos la respuesta directa
        return response_message.content