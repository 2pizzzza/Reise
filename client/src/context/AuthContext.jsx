// src/context/AuthContext.jsx
import React, { createContext, useContext, useState } from 'react';
import AuthService from '../services/AuthService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const register = async (name, email, password) => {
        const data = await AuthService.register(name, email, password);
        setUser(data);
        localStorage.setItem('token', data.access_token); // Сохранение токена в локальном хранилище
    };

    const login = async (email, password) => {
        const data = await AuthService.login(email, password);
        setUser(data);
        localStorage.setItem('token', data.access_token); // Сохранение токена в локальном хранилище
    };

    return (
        <AuthContext.Provider value={{ user, register, login }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
