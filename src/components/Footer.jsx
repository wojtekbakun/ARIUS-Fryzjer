import 'react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section contact">
                    <h3>Kontakt</h3>
                    <p>Adres: ul. Przykładowa 123, Warszawa</p>
                    <p>Telefon: +48 123 456 789</p>
                    <p>Email: kontakt@fryzjerski.pl</p>
                </div>
                <div className="footer-section location">
                    <h3>Godziny otwarcia</h3>
                    <p>Poniedziałek - Piątek: 9:00 - 20:00</p>
                    <p>Sobota: 9:00 - 18:00</p>
                    <p>Niedziela: Zamknięte</p>
                </div>
                <div className="footer-section socials">
                    <h3>Obserwuj nas</h3>
                    <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">
                        <i className="fab fa-facebook"></i> Facebook
                    </a>
                    <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">
                        <i className="fab fa-instagram"></i> Instagram
                    </a>
                    <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer">
                        <i className="fab fa-twitter"></i> Twitter
                    </a>
                </div>

            </div>
            <div className="footer-bottom">
                <p>&copy; 2025 fryzjerski® - Wszystkie prawa zastrzeżone</p>
            </div>
        </footer>
    );
};

export default Footer;
