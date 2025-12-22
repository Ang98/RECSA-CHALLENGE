import { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { sendMessage, type Message } from './chatService';

interface ChatPageProps {
  onLogout: () => void;
}

export const ChatPage = ({ onLogout }: ChatPageProps) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: '¡Hola! Soy tu asistente médico virtual. ¿En qué puedo ayudarte hoy?' }
  ]);
  
  // Referencia para el scroll automático
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Hook de mutación para enviar el mensaje
  const { mutate, isPending } = useMutation({
    mutationFn: (text: string) => sendMessage(text, messages),
    onSuccess: (data) => {
      // Agregamos la respuesta del bot al historial visual
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }]);
    },
    onError: () => {
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Lo siento, tuve un error de conexión. Intenta de nuevo.' }]);
    }
  });

  // Efecto para bajar el scroll cada vez que llega un mensaje nuevo
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isPending]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isPending) return;

    const userMsg = input.trim();
    
    // 1. Agregamos optimísticamente el mensaje del usuario
    setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
    setInput('');

    // 2. Enviamos al backend
    mutate(userMsg);
  };

  return (
    <div className="flex h-screen flex-col bg-gray-100">
      {/* HEADER */}
      <header className="flex items-center justify-between bg-blue-600 px-6 py-4 text-white shadow-md">
        <div>
          <h1 className="text-xl font-bold">Asistente Médico RECSA</h1>
          <p className="text-xs text-blue-100">Impulsado por OpenAI & Django</p>
        </div>
        <button 
          onClick={onLogout}
          className="rounded bg-blue-700 px-3 py-1 text-sm font-medium hover:bg-blue-800 transition"
        >
          Cerrar Sesión
        </button>
      </header>

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2 shadow-sm ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
              }`}
            >
              <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
            </div>
          </div>
        ))}

        {/* Indicador de "Escribiendo..." */}
        {isPending && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl px-4 py-2 border border-gray-200 rounded-bl-none shadow-sm">
              <div className="flex space-x-1 h-5 items-center">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* INPUT AREA */}
      <div className="bg-white p-4 shadow-lg border-t border-gray-200">
        <form onSubmit={handleSend} className="mx-auto max-w-4xl flex gap-2">
          <input
            type="text"
            className="flex-1 rounded-full border border-gray-300 bg-gray-50 px-4 py-3 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="Escribe tu mensaje aquí..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isPending}
          />
          <button
            type="submit"
            disabled={isPending || !input.trim()}
            className="rounded-full bg-blue-600 p-3 text-white transition hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {/* Ícono de enviar (SVG) */}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
              <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};