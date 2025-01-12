import { useState, useEffect } from 'react';
import axios from '../api/axios';
import './ProfilePage.css';

import ProfileHistory from './ProfileHistory';
import ProfileReviews from './ProfileReviews';

const ProfilePage = () => {
    const [profileData, setProfileData] = useState({});
    const [activeTab, setActiveTab] = useState('Dane');
    const [errorMessage, setErrorMessage] = useState('');
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
        street: '',
        street_number: '',
        postal_code: '',
        city: '',
        nip: '',
        company_name: '',
    });
    const [canReview, setCanReview] = useState(false);
    const [reviewData, setReviewData] = useState({
        service_id: '',
        rating: 5,
        comment: '',
    });
    const [reviewMessage, setReviewMessage] = useState('');

    /* Wczytanie danych profilu */
    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await axios.get('/user/profile');
                setProfileData(response.data);
                setFormData({
                    first_name: response.data.first_name || '',
                    last_name: response.data.last_name || '',
                    email: response.data.email || '',
                    street: response.data.street || '',
                    street_number: response.data.street_number || '',
                    postal_code: response.data.postal_code || '',
                    city: response.data.city || '',
                    nip: response.data.nip || '',
                    company_name: response.data.company_name || '',
                    password: '', // Pole hasło zostawiamy puste
                    confirm_password: '',
                });

                // Sprawdzenie, czy użytkownik ma zakończone wizyty, aby móc dodać opinię
                const appointmentsResponse = await axios.get('/appointments/all', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                const hasCompletedAppointments = appointmentsResponse.data.some(
                    (appointment) => new Date(appointment.date) < new Date() && !appointment.reviewed
                );
                setCanReview(hasCompletedAppointments);
            } catch (error) {
                setErrorMessage('Nie udało się pobrać danych użytkownika.');
                console.error('Błąd podczas pobierania danych użytkownika:', error);
            }
        };

        fetchProfile();
    }, []);

    /* Zmiana aktywnej zakładki */
    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setEditMode(false); // na wszelki wypadek wyłączamy tryb edycji
    };

    /* Obsługa zmian w inputach */
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    /* Zapis danych po edycji */
    const handleSaveChanges = async (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirm_password) {
            alert('Hasło musi się zgadzać w obu polach!');
            return;
        }

        try {
            const updateData = { ...formData };

            // Jeśli hasło nie zostało zmienione, usuń je z wysyłanych danych
            if (!updateData.password) {
                delete updateData.password;
            }
            // Usuwamy pole potwierdzenia hasła przed wysłaniem
            delete updateData.confirm_password;

            await axios.post('/user/profile', updateData);
            setProfileData(updateData);
            setEditMode(false);
            alert('Dane zostały zaktualizowane.');
        } catch (error) {
            alert('Nie udało się zaktualizować danych.');
            console.error('Błąd podczas zapisywania danych użytkownika:', error);
        }
    };

    /* Wylogowanie */
    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login';
    };

    /* Obsługa zmian w formularzu opinii */
    const handleReviewChange = (e) => {
        const { name, value } = e.target;
        setReviewData({ ...reviewData, [name]: value });
    };

    /* Zapis opinii */
    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        setReviewMessage('');

        try {
            await axios.post('/reviews/review', reviewData);
            setReviewMessage('Twoja opinia została dodana!');
            setReviewData({
                service_id: '',
                rating: 5,
                comment: '',
            });
        } catch (error) {
            setReviewMessage('Wystąpił błąd podczas dodawania opinii.');
            console.error('Błąd podczas dodawania opinii:', error);
        }
    };

    return (
        <div className="profile-page">
            <h1>Twój Profil</h1>

            {errorMessage && <p className="error-message">{errorMessage}</p>}

            {/* Nawigacja (zakładki) */}
            <div className="profile-nav">
                <button
                    className={activeTab === 'Dane' ? 'active' : ''}
                    onClick={() => handleTabChange('Dane')}
                >
                    Dane
                </button>
                <button
                    className={activeTab === 'Wizyty' ? 'active' : ''}
                    onClick={() => handleTabChange('Wizyty')}
                >
                    Wizyty
                </button>
                <button
                    className={activeTab === 'Oceny' ? 'active' : ''}
                    onClick={() => handleTabChange('Oceny')}
                >
                    Oceny
                </button>
            </div>

            {/* Treść każdej zakładki */}
            {activeTab === 'Dane' && (
                <div className="profile-data">
                    {!editMode ? (
                        <>
                            <p>
                                <strong>Imię:</strong> {profileData.first_name || 'Nie podano'}
                            </p>
                            <p>
                                <strong>Nazwisko:</strong> {profileData.last_name || 'Nie podano'}
                            </p>
                            <p>
                                <strong>Email:</strong> {profileData.email || 'Nie podano'}
                            </p>
                            <p>
                                <strong>Adres:</strong> {profileData.street || 'Nie podano'}, {profileData.street_number || 'Nie podano'}
                            </p>
                            <p>
                                <strong>Kod pocztowy:</strong> {profileData.postal_code || 'Nie podano'}
                            </p>
                            <p>
                                <strong>Miasto:</strong> {profileData.city || 'Nie podano'}
                            </p>
                            <p>
                                <strong>Nazwa firmy:</strong> {profileData.company_name || 'Nie podano'}
                            </p>
                            <p>
                                <strong>NIP:</strong> {profileData.nip || 'Nie podano'}
                            </p>

                            <button onClick={() => setEditMode(true)}>Zmień dane</button>
                        </>
                    ) : (
                        <form className="edit-form" onSubmit={handleSaveChanges}>
                            <label>
                                Imię:
                                <input
                                    type="text"
                                    name="first_name"
                                    value={formData.first_name}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Nazwisko:
                                <input
                                    type="text"
                                    name="last_name"
                                    value={formData.last_name}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Email:
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Nowe hasło:
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleInputChange}
                                    placeholder="Nowe hasło"
                                />
                            </label>
                            <label>
                                Potwierdź hasło:
                                <input
                                    type="password"
                                    name="confirm_password"
                                    value={formData.confirm_password}
                                    onChange={handleInputChange}
                                    placeholder="Potwierdź hasło"
                                />
                            </label>
                            <label>
                                Ulica:
                                <input
                                    type="text"
                                    name="street"
                                    value={formData.street}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Numer ulicy:
                                <input
                                    type="text"
                                    name="street_number"
                                    value={formData.street_number}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Kod pocztowy:
                                <input
                                    type="text"
                                    name="postal_code"
                                    value={formData.postal_code}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Miasto:
                                <input
                                    type="text"
                                    name="city"
                                    value={formData.city}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Nazwa firmy:
                                <input
                                    type="text"
                                    name="company_name"
                                    value={formData.company_name}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                NIP:
                                <input
                                    type="text"
                                    name="nip"
                                    value={formData.nip}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <div className="form-buttons">
                                <button type="submit">Zapisz</button>
                                <button type="button" onClick={() => setEditMode(false)}>Anuluj</button>
                            </div>
                        </form>
                    )}
                </div>
            )}

            {activeTab === 'Wizyty' && (
                /* Wczytujemy komponent z historią wizyt */
                <ProfileHistory />
            )}

            {activeTab === 'Oceny' && (
                /* Wczytujemy komponent z opiniami użytkowników */
                <ProfileReviews />
            )}

            {canReview && activeTab === 'Oceny' && (
                /* Formularz dodawania opinii w profilu */
                <div className="add-review-form">
                    <h3>Dodaj swoją opinię</h3>
                    {reviewMessage && <p className={reviewMessage.includes('błąd') ? 'error-message' : 'success-message'}>{reviewMessage}</p>}
                    <form onSubmit={handleReviewSubmit}>
                        <label>
                            Wybierz usługę:
                            <select
                                name="service_id"
                                value={reviewData.service_id}
                                onChange={handleReviewChange}
                                required
                            >
                                <option value="">-- Wybierz usługę --</option>
                                {profileData.services && profileData.services.map(service => (
                                    <option key={service.id} value={service.id}>
                                        {service.name}
                                    </option>
                                ))}
                            </select>
                        </label>
                        <label>
                            Ocena:
                            <select
                                name="rating"
                                value={reviewData.rating}
                                onChange={handleReviewChange}
                                required
                            >
                                {[1, 2, 3, 4, 5].map(num => (
                                    <option key={num} value={num}>{num} gwiazdek</option>
                                ))}
                            </select>
                        </label>
                        <label>
                            Komentarz (opcjonalny):
                            <textarea
                                name="comment"
                                value={reviewData.comment}
                                onChange={handleReviewChange}
                                placeholder="Twoja opinia..."
                            ></textarea>
                        </label>
                        <button type="submit">Dodaj opinię</button>
                    </form>
                </div>
            )}

            <button className="logout-button" onClick={handleLogout}>
                Wyloguj się
            </button>
        </div>
    );

};

export default ProfilePage;
