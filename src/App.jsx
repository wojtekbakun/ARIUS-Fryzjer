import 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import AboutPage from './pages/AboutPage.jsx';
import ServicesPage from './pages/ServicesPage.jsx';
import LoginPage from './pages/LoginPage';
import ReviewsPage from './pages/ReviewsPage.jsx';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage.jsx';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import AppointmentPage from './pages/AppointmentPage';
import HairdressersPage from './pages/HairdressersPage';

// Komponent chroniący trasy
const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token');
    return token ? children : <Navigate to="/login" />;
};

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
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route
                    path="/profile"
                    element={
                        <ProtectedRoute>
                            <ProfilePage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/appointment"
                    element={
                        <ProtectedRoute>
                            <AppointmentPage />
                        </ProtectedRoute>
                    }
                />
                <Route path="/hairdressers" element={<HairdressersPage />} />
                {/* Dodaj inne trasy tutaj */}
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
            <Footer />
        </Router>
    );
};

export default App;
