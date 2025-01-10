import 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import AboutPage from './pages/AboutPage.jsx';
import Footer from './components/Footer';
import ServicesPage from "./pages/ServicesPage.jsx";
import LoginPage from './pages/LoginPage';
import ReviewsPage from './pages/ReviewsPage.jsx';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage.jsx'; // Import ProfilePage
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import AppointmentPage from './pages/AppointmentPage';
import HairdressersPage from './pages/HairdressersPage';
const App = () => {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/services" element={<ServicesPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/reviews" element={<ReviewsPage />} />
                <Route path="/profile" element={<ProfilePage />} /> {/* Nowa ścieżka */}
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route path="/appointment" element={<AppointmentPage />} />
                <Route path="/hairdressers" element={<HairdressersPage />} />
            </Routes>
            <Footer />
        </Router>
    );
};

export default App;
