import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Register from './components/Auth/Register';
import Login from './components/Auth/Login';
import Navbar from './components/Layout/Navbar';
import Home from './pages/Home';
import Profile from './pages/Profile';

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/my-profile" element={<Profile isOwnProfile={true} />} />
                    <Route path="/profile/:username" element={<Profile />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;
