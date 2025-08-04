import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider');
  }
  return context;
};

// Configurar axios baseURL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
axios.defaults.baseURL = API_URL;

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('cineai_token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Configurar interceptor do axios
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Interceptor para responses
  useEffect(() => {
    const responseInterceptor = axios.interceptors.response.add(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          logout();
        }
        return Promise.reject(error);
      }
    );

    return () => axios.interceptors.response.eject(responseInterceptor);
  }, []);

  // Verificar token válido na inicialização
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await axios.get('/api/auth/me');
          setUser(response.data.user);
          setError(null);
        } catch (error) {
          console.error('Token inválido:', error);
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token]);

  const login = async (email, password) => {
    try {
      setError(null);
      setLoading(true);
      
      const response = await axios.post('/api/auth/login', {
        email,
        password
      });

      const { user, token } = response.data;
      
      setUser(user);
      setToken(token);
      localStorage.setItem('cineai_token', token);
      
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erro ao fazer login';
      setError(errorMessage);
      return {
        success: false,
        error: errorMessage
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (name, email, password) => {
    try {
      setError(null);
      setLoading(true);
      
      const response = await axios.post('/api/auth/register', {
        name,
        email,
        password
      });

      const { user, token } = response.data;
      
      setUser(user);
      setToken(token);
      localStorage.setItem('cineai_token', token);
      
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erro ao criar conta';
      setError(errorMessage);
      return {
        success: false,
        error: errorMessage
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setError(null);
    localStorage.removeItem('cineai_token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const updateProfile = async (profileData) => {
    try {
      setError(null);
      const response = await axios.put('/api/auth/profile', profileData);
      setUser(response.data.user);
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erro ao atualizar perfil';
      setError(errorMessage);
      return {
        success: false,
        error: errorMessage
      };
    }
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      setError(null);
      await axios.post('/api/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erro ao alterar senha';
      setError(errorMessage);
      return {
        success: false,
        error: errorMessage
      };
    }
  };

  const clearError = () => setError(null);

  const value = {
    user,
    token,
    loading,
    error,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    clearError,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};