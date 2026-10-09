import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../api/apiClient';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem('campusiq_token');
    const savedUser = localStorage.getItem('campusiq_user');
    if (savedToken && savedUser) {
      try {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('campusiq_token');
        localStorage.removeItem('campusiq_user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    const data = response.data;
    const userData = {
      user_id: data.user_id,
      name: data.name,
      email: data.email,
      role: data.role,
      student_id: data.student_id,
      faculty_id: data.faculty_id,
    };
    localStorage.setItem('campusiq_token', data.access_token);
    localStorage.setItem('campusiq_user', JSON.stringify(userData));
    setToken(data.access_token);
    setUser(userData);
    return userData;
  };

  const register = async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('campusiq_token');
    localStorage.removeItem('campusiq_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, role: user?.role, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
