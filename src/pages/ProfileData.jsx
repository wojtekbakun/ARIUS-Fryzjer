import React, { useState, useEffect } from 'react';
import axios from '../api/axios';

const ProfileData = () => {
    const [userData, setUserData] = useState({
        firstName: '',
        lastName: '',
        address: '',
        email: '',
    });
    const [isEditing, setIsEditing] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('/user/profile', {
                    headers: { Authorization: `Bearer ${token}` },
                });
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
            const token = localStorage.getItem('token');
            const response = await axios.post('/user/profile', userData, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (response.status === 200) {
                setMessage('Dane zostały zapisane pomyślnie.');
                setIsEditing(false);
            } else {
                setMessage('Wystąpił błąd podczas zapisywania danych.');
            }
        } catch (error) {
            console.error('Błąd podczas zapisywania danych użytkownika:', error);
            setMessage('Wystąpił błąd podczas zapisywania danych.');
        }
    };




    return (
        <div className="profile-data">
            <h2>Dane użytkownika</h2>
            {message && <p style={{ color: 'green' }}>{message}</p>}
            {!isEditing ? (
                <div>
                    <p>
                        <strong>Imię:</strong> {userData.firstName}
                    </p>
                    <p>
                        <strong>Nazwisko:</strong> {userData.lastName}
                    </p>
                    <p>
                        <strong>Adres:</strong> {userData.address}
                    </p>
                    <p>
                        <strong>Email:</strong> {userData.email}
                    </p>
                    <button
                        onClick={() => setIsEditing(true)}
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
                        Zmień dane
                    </button>
                </div>
            ) : (
                <form onSubmit={handleSaveChanges}>
                    <label>
                        Imię:
                        <input
                            type="text"
                            name="firstName"
                            value={userData.firstName}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Nazwisko:
                        <input
                            type="text"
                            name="lastName"
                            value={userData.lastName}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                    <label>
                        Adres:
                        <input
                            type="text"
                            name="address"
                            value={userData.address}
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
                        Zapisz zmiany
                    </button>
                    <button
                        type="button"
                        onClick={() => setIsEditing(false)}
                        style={{
                            marginLeft: '1rem',
                            padding: '0.5rem 1rem',
                            backgroundColor: '#ccc',
                            color: '#000',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer',
                        }}
                    >
                        Anuluj
                    </button>
                </form>
            )}
        </div>
    );
};

export default ProfileData;
