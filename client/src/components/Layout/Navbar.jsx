import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles.css';

const Navbar = () => {
    return (
        <nav>
            <Link to="/">Главная</Link>
            <Link to="/profile">Профиль</Link>
            <Link to="/search">Поиск</Link>
        </nav>
    );
};

export default Navbar;
