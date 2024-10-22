// src/services/AuthService.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/auth/';

const register = async (name, email, password) => {
    const response = await axios.post(`${API_URL}signup`, { name, email, password });
    return response.data;
};

const login = async (email, password) => {
    const response = await axios.post(`${API_URL}signin`, { email, password });
    return response.data;
};

export default {
    register,
    login,
};
