import React, { createContext, useState, useEffect } from 'react';
import API from '../api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  useEffect(() => {
    // Al cargar la app, verificamos si hay un usuario guardado en el navegador
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
      return { 
        success: false, 
        message: error.response?.data?.detail || "Credenciales incorrectas" 
      };
    }
  };

  const register = async (username, email, password) => {
    try {
      await API.post('/auth/register/', { username, email, password });
      // Tras registrar con éxito, lo mandamos al login automáticamente
      return await login(username, password);
    } catch (error) {
      const errors = error.response?.data;
      let errorMsg = "Error en el registro";
      if (errors) {
        errorMsg = Object.values(errors).flat().join(" ");
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