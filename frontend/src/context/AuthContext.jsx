import React, { createContext, useState, useEffect } from 'react';
import API from '../api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('username');
    const token = localStorage.getItem('accessToken');
    if (storedUser && token) {
      setUser({ username: storedUser });
    }
    setAuthLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await API.post('/auth/token/', { username, password });
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      localStorage.setItem('username', username);
      setUser({ username });
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail 
        || "Credenciales incorrectas o ruta no encontrada";
      return { success: false, message };
    }
  };

  const register = async (username, email, password) => {
    try {
      await API.post('/auth/register/', { username, email, password });
      return await login(username, password);
    } catch (error) {
      const errors = error.response?.data;
      let errorMsg = "Error al conectar con el servidor (404 o sin conexión)";

      if (errors) {
        if (typeof errors === 'string') {
          errorMsg = errors;
        } else if (errors.detail) {
          errorMsg = errors.detail;
        } else if (typeof errors === 'object') {
          errorMsg = Object.entries(errors)
            .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(' ') : val}`)
            .join(' | ');
        }
      }
      
      return { success: false, message: errorMsg };
    }
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, authLoading }}>
      {children}
    </AuthContext.Provider>
  );
}