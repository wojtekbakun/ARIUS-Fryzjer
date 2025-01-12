import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axios';

const RegisterPage = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        street: '',
        street_number: '',
        postal_code: '',
        city: '',
        nip: '',
        company_name: '',
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        if (formData.password !== formData.confirmPassword) {
            setError('Hasła się nie zgadzają.');
            return;
        }
        try {
            // Wysyłanie danych do backendu
            const payload = {
                email: formData.email,
                password: formData.password,
                street: formData.street || null,
                street_number: formData.street_number || null,
                postal_code: formData.postal_code || null,
                city: formData.city || null,
                nip: formData.nip || null,
                company_name: formData.company_name || null,
            };

            await axios.post('/auth/register', payload);

            // Przekierowanie na stronę logowania po rejestracji
            navigate('/login');
        } catch (err) {
            // Obsługa błędów rejestracji
            setError(err.response?.data?.message || 'Błąd podczas rejestracji. Spróbuj ponownie.');
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto' }}>
            <h2>Rejestracja</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Imię:</label>
                    <input
                        type="text"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        required
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Nazwisko:</label>
                    <input
                        type="text"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        required
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                        style={{ padding: '0.5rem', width: '100%' }}
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
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Potwierdź hasło:</label>
                    <input
                        type="password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        required
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Ulica:</label>
                    <input
                        type="text"
                        name="street"
                        value={formData.street}
                        onChange={handleInputChange}
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Numer ulicy:</label>
                    <input
                        type="text"
                        name="street_number"
                        value={formData.street_number}
                        onChange={handleInputChange}
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Kod pocztowy:</label>
                    <input
                        type="text"
                        name="postal_code"
                        value={formData.postal_code}
                        onChange={handleInputChange}
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Miasto:</label>
                    <input
                        type="text"
                        name="city"
                        value={formData.city}
                        onChange={handleInputChange}
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>NIP:</label>
                    <input
                        type="text"
                        name="nip"
                        value={formData.nip}
                        onChange={handleInputChange}
                        style={{ padding: '0.5rem', width: '100%' }}
                    />
                </div>
                <div>
                    <label>Nazwa firmy:</label>
                    <input
                        type="text"
                        name="company_name"
                        value={formData.company_name}
                        onChange={handleInputChange}
                        style={{ padding: '0.5rem', width: '100%' }}
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
                    Zarejestruj się
                </button>
            </form>
        </div>
    );
};

export default RegisterPage;
