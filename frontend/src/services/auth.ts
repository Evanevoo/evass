import api from './api';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  phone_number?: string;
  address?: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/login', credentials);
  return response.data;
};

export const register = async (data: RegisterData): Promise<void> => {
  await api.post('/users/register', data);
};

export const logout = (): void => {
  localStorage.removeItem('token');
  window.location.href = '/login';
};

export const getCurrentUser = async () => {
  const response = await api.get('/users/me');
  return response.data;
};

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('token');
}; 