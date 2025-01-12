import 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';

const Header = () => {
    const token = localStorage.getItem('token');
    const navigate = useNavigate();

    const handleProtectedNavigation = (path) => {
        if (token) {
            navigate(path);
        } else {
            navigate('/login');
        }
    };

    return (
        <header className="header">
            {/* Główny kontener wewnątrz nagłówka */}
            <div className="header-container">
                <div className="logo">
                    <Link to="/" className="logo-link">
                        fryzjerski<sup>®</sup>
                    </Link>
                </div>
                <nav className="nav">
                    <ul className="nav-list">
                        <li><Link to="/about">O nas</Link></li>
                        <li><Link to="/services">Usługi</Link></li>
                        <li><Link to="/hairdressers">Fryzjerzy</Link></li>
                        <li><Link to="/reviews">Opinie</Link></li>
                        <li><Link to="/profile">Profil</Link></li>
                        <li>
                            <button
                                className="cta-button"
                                onClick={() => handleProtectedNavigation('/appointment')}
                            >
                                Umów wizytę
                            </button>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    );
};

export default Header;
