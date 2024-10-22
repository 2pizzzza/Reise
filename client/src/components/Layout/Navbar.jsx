import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles.css';

const Navbar = () => {
    return (
        <nav>
            <Link to="/">Главная</Link>
            <li><Link to="/my-profile">Мой профиль</Link></li> {/* Ссылка на свой профиль */}
            <Link to="/search">Поиск</Link>
        </nav>
    );
};

export default Navbar;
