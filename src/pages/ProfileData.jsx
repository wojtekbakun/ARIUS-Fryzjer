import { useState, useEffect } from 'react';
import axios from '../api/axios';
import './ProfileData.css';

const ProfileData = () => {
    const [userData, setUserData] = useState({
        first_name: '',
        last_name: '',
        street: '',
        street_number: '',
        postal_code: '',
        city: '',
        nip: '',
        company_name: '',
        email: '',
    });
    const [isEditing, setIsEditing] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await axios.get('/user/profile');
                setUserData(response.data);
            } catch (error) {
                console.error('Błąd podczas pobierania danych użytkownika:', error);
            }
        };
        fetchUserData();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUserData({ ...userData, [name]: value });
    };

    const handleSaveChanges = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/user/profile', userData);
            setMessage('Dane zostały zapisane pomyślnie.');
            setIsEditing(false);
        } catch (error) {
            console.error('Błąd podczas zapisywania danych użytkownika:', error);
            setMessage('Wystąpił błąd podczas zapisywania danych.');
        }
    };

    return (
        <div className="profile-data">
            <h2>Dane użytkownika</h2>
            {message && <p className="message">{message}</p>}
            {!isEditing ? (
                <div>
                    <p><strong>Imię:</strong> {userData.first_name || 'Nie podano'}</p>
                    <p><strong>Nazwisko:</strong> {userData.last_name || 'Nie podano'}</p>
                    <p><strong>Email:</strong> {userData.email || 'Nie podano'}</p>
                    <p><strong>Adres:</strong> {userData.street || 'Nie podano'}, {userData.street_number || 'Nie podano'}</p>
                    <p><strong>Kod pocztowy:</strong> {userData.postal_code || 'Nie podano'}</p>
                    <p><strong>Miasto:</strong> {userData.city || 'Nie podano'}</p>
                    <p><strong>Nazwa firmy:</strong> {userData.company_name || 'Nie podano'}</p>
                    <p><strong>NIP:</strong> {userData.nip || 'Nie podano'}</p>
                    <button onClick={() => setIsEditing(true)}>Zmień dane</button>
                </div>
            ) : (
                <form onSubmit={handleSaveChanges}>
                    <label>
                        Imię:
                        <input
                            type="text"
                            name="first_name"
                            value={userData.first_name}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Nazwisko:
                        <input
                            type="text"
                            name="last_name"
                            value={userData.last_name}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Email:
                        <input
                            type="email"
                            name="email"
                            value={userData.email}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Ulica:
                        <input
                            type="text"
                            name="street"
                            value={userData.street}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Numer ulicy:
                        <input
                            type="text"
                            name="street_number"
                            value={userData.street_number}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Kod pocztowy:
                        <input
                            type="text"
                            name="postal_code"
                            value={userData.postal_code}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Miasto:
                        <input
                            type="text"
                            name="city"
                            value={userData.city}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Nazwa firmy:
                        <input
                            type="text"
                            name="company_name"
                            value={userData.company_name}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        NIP:
                        <input
                            type="text"
                            name="nip"
                            value={userData.nip}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <div className="form-buttons">
                        <button type="submit">Zapisz</button>
                        <button type="button" onClick={() => setIsEditing(false)}>Anuluj</button>
                    </div>
                </form>
            )}
        </div>
    );
};

export default ProfileData;
