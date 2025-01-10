import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
    return (
        <header className="header">
            <div className="logo">
                <Link to="/" className="logo-link">
                    fryzjerski<sup>®</sup>
                </Link>
            </div>
            <nav className="nav">
                <ul className="nav-list">
                    <li><Link to="/about">O nas</Link></li>
                    <li><Link to="/services">Usługi</Link></li>
                    <li><Link to="/contact">Kontakt</Link></li>
                    <li><Link to="/hairdressers">Fryzjerzy</Link></li> {/* Dodano Fryzjerzy */}
                    <li><Link to="/profile">Profil</Link></li>
                    <li><Link to="/appointment" className="cta-button">Umów wizytę</Link></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
