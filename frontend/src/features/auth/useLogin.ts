import { useMutation } from '@tanstack/react-query';
import { loginUser } from './authService';

export const useLogin = () => {
  return useMutation({
    mutationFn: ({ user, pass }: { user: string; pass: string }) => 
      loginUser(user, pass),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
    },
  });
};