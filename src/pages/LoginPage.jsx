import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axios';

const LoginPage = () => {
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await axios.post('/auth/login', formData);
            localStorage.setItem('token', response.data.token); // Zapisanie tokenu w localStorage
            navigate('/profile'); // Przekierowanie na profil
        } catch (err) {
            setError(err.response?.data?.message || 'Błąd logowania. Sprawdź dane i spróbuj ponownie.');
        }
    };

    return (
        <div style={{padding: '2rem', maxWidth: '400px', margin: '0 auto'}}>
            <h2>Logowanie</h2>
            {error && <p style={{color: 'red'}}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                        style={{padding: '0.5rem', width: '100%'}}
                    />
                </div>
                <div>
                    <label>Hasło:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        required
                        style={{padding: '0.5rem', width: '100%'}}
                    />
                </div>
                <button
                    type="submit"
                    style={{
                        marginTop: '1rem',
                        padding: '0.5rem 1rem',
                        backgroundColor: '#000',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                    }}
                >
                    Zaloguj się
                </button>
            </form>
            <p style={{marginTop: '1rem', textAlign: 'center'}}>
                Nie masz konta?{' '}
                <button
                    onClick={() => navigate('/register')}
                    style={{
                        background: 'none',
                        color: 'blue',
                        border: 'none',
                        cursor: 'pointer',
                        textDecoration: 'underline',
                    }}
                >
                    Zarejestruj się
                </button>
            </p>

        </div>
    );
};

export default LoginPage;
