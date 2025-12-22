import api from '../../services/api';

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatResponse {
  response: string;
}

export const sendMessage = async (message: string, history: Message[]) => {
  // Enviamos el mensaje actual y el historial previo
  const { data } = await api.post<ChatResponse>('/chat/', {
    message,
    history,
  });
  return data;
};