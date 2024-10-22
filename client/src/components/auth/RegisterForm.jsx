import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../../services/auth.service';

export const RegisterForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await AuthService.register(formData.name, formData.email, formData.password);
      navigate('/login');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8">
      <div className="mb-4">
        <input
          type="text"
          placeholder="Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full p-2 border rounded"
        />
      </div>
      <div className="mb-4">
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="w-full p-2 border rounded"
        />
      </div>
      <div className="mb-4">
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          className="w-full p-2 border rounded"
        />
      </div>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
        Register
      </button>
    </form>
  );
};