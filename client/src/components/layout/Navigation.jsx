import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthService } from '../../services/auth.service';

export const Navigation = () => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    AuthService.logout();
    navigate('/login');
  };

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex space-x-4">
          <Link to="/" className="hover:text-gray-300">Главная</Link>
          <Link to="/search" className="hover:text-gray-300">Поиск</Link>
          <Link to="/profile" className="hover:text-gray-300">Профиль</Link>
        </div>
        <button
          onClick={handleLogout}
          className="bg-red-500 px-4 py-2 rounded hover:bg-red-600"
        >
          Выйти
        </button>
      </div>
    </nav>
  );
};
