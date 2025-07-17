import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { authService } from '@/services/auth';

interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

interface RegisterData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  // Mock user for development - remove this in production
  const mockUser: User = {
    id: '1',
    email: 'demo@autoredact.ai',
    username: 'demo_user',
    full_name: 'Demo User',
    role: 'admin',
    is_active: true,
    is_verified: true,
  };

  const [user, setUser] = useState<User | null>(mockUser); // Set mock user as default
  const [isLoading, setIsLoading] = useState(false); // Set to false since we have mock user
  const queryClient = useQueryClient();

  // Comment out the real authentication check for development
  // const { data: currentUser, isLoading: userLoading } = useQuery(
  //   'currentUser',
  //   authService.getCurrentUser,
  //   {
  //     retry: false,
  //     onSuccess: (data) => {
  //       setUser(data);
  //     },
  //     onError: () => {
  //       setUser(null);
  //     },
  //   }
  // );

  // Login mutation
  const loginMutation = useMutation(
    ({ email, password }: { email: string; password: string }) =>
      authService.login(email, password),
    {
      onSuccess: (data) => {
        // Store tokens
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        
        // Fetch user data
        queryClient.invalidateQueries('currentUser');
      },
      onError: (error) => {
        console.error('Login failed:', error);
        throw error;
      },
    }
  );

  // Register mutation
  const registerMutation = useMutation(
    (userData: RegisterData) => authService.register(userData),
    {
      onSuccess: (data) => {
        // Optionally auto-login after registration
        console.log('Registration successful:', data);
      },
      onError: (error) => {
        console.error('Registration failed:', error);
        throw error;
      },
    }
  );

  // Logout function
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    queryClient.clear();
  };

  // Refresh token function
  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const data = await authService.refreshToken(refreshToken);
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      
      // Refetch user data
      queryClient.invalidateQueries('currentUser');
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      throw error;
    }
  };

  // Login function
  const login = async (email: string, password: string) => {
    await loginMutation.mutateAsync({ email, password });
  };

  // Register function
  const register = async (userData: RegisterData) => {
    await registerMutation.mutateAsync(userData);
  };

  // Set loading state
  useEffect(() => {
    setIsLoading(false); // Set to false since we have mock user
  }, []);

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    refreshToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 