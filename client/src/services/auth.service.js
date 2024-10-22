const API_URL = 'http://127.0.0.1:8000/auth';

export const AuthService = {
  async login(email, password) {
    const response = await fetch(`${API_URL}/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      return data;
    }
    throw new Error(data.message);
  },

  async register(name, email, password) {
    const response = await fetch(`${API_URL}/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message);
    }
    return data;
  },

  logout() {
    localStorage.removeItem('token');
  }
};