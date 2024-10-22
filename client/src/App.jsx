import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LoginForm } from './components/auth/LoginForm';
import { RegisterForm } from './components/auth/RegisterForm';
import { Navigation } from './components/layout/Navigation';
import { Home } from './pages/Home';
import { Profile } from './pages/Profile';
import { Search } from './pages/Search';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

export const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <>
                <Navigation />
                <Home />
              </>
            </PrivateRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <>
                <Navigation />
                <Profile />
              </>
            </PrivateRoute>
          }
        />
        <Route
          path="/search"
          element={
            <PrivateRoute>
              <>
                <Navigation />
                <Search />
              </>
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
};