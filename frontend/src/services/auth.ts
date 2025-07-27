import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  full_name: string;
  password: string;
}

class AuthService {
  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post('/api/v1/auth/login', {
      email,
      password,
    });
    
    const { access_token, token_type, user } = response.data;
    localStorage.setItem('token', access_token);
    
    return { access_token, token_type, user };
  }

  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await api.post('/api/v1/auth/register', data);
    
    const { access_token, token_type, user } = response.data;
    localStorage.setItem('token', access_token);
    
    return { access_token, token_type, user };
  }

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/api/v1/auth/me');
    return response.data;
  }

  logout(): void {
    localStorage.removeItem('token');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
}

export const authService = new AuthService(); 