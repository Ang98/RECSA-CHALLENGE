import api from '../../services/api';

export const loginUser = async (email: string, password: string) => {
  // Nota la ruta: /token/ es la que definimos en Django
  const response = await api.post('/token/', { email, password });
  return response.data; // Retorna { access: "...", refresh: "..." }
};