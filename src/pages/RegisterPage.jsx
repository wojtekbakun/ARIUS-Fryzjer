import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axios';

const RegisterPage = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        if (formData.password !== formData.confirmPassword) {
            setError('Hasła nie są zgodne!');
            return;
        }

        try {
            await axios.post('/auth/register', {
                firstName: formData.firstName,
                lastName: formData.lastName,
                email: formData.email,
                password: formData.password,
            });
            setSuccess('Rejestracja zakończona sukcesem! Przekierowuję na logowanie...');
            setTimeout(() => navigate('/login'), 2000); // Przekierowanie po 2 sekundach
        } catch (err) {
            setError(err.response?.data?.message || 'Błąd podczas rejestracji. Spróbuj ponownie.');
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto' }}>
            <h2>Rejestracja</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="firstName"
                    placeholder="Imię"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                    style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
                />
                <input
                    type="text"
                    name="lastName"
                    placeholder="Nazwisko"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                    style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Hasło"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                    style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
                />
                <input
                    type="password"
                    name="confirmPassword"
                    placeholder="Potwierdź hasło"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                    style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
                />
                <button
                    type="submit"
                    style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: '#000',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                    }}
                >
                    Zarejestruj się
                </button>
            </form>
        </div>
    );
};

export default RegisterPage;
