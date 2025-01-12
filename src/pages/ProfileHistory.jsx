import { useState, useEffect } from 'react';
import apiClient from '../api/axios';
import './ProfileHistory.css';

const ProfileHistory = () => {
    const [tab, setTab] = useState('upcoming'); // upcoming | history
    const [appointments, setAppointments] = useState([]);
    const [error, setError] = useState('');


    const handleSendInvoice = async (appointmentId) => {
        try {
            await apiClient.post('/payments/send-invoice', { appointment_id: appointmentId });
            alert('Faktura wysłana na maila.');
        } catch (err) {
            console.error('Błąd podczas wysyłania faktury:', err);
            alert('Wystąpił błąd podczas wysyłania faktury.');
        }
    };

    useEffect(() => {
        const fetchAppointments = async () => {
            try {
                // Pobierz wszystkie wizyty
                const response = await apiClient.get('/appointments/all');
                let filteredAppointments = [];

                if (tab === 'upcoming') {
                    // Przyszłe wizyty
                    filteredAppointments = response.data.filter(
                        (appointment) => new Date(appointment.date) >= new Date()
                    );
                } else if (tab === 'history') {
                    // Odbyte wizyty
                    filteredAppointments = response.data.filter(
                        (appointment) => new Date(appointment.date) < new Date()
                    );
                }

                setAppointments(filteredAppointments);
            } catch (err) {
                setError('Błąd podczas ładowania wizyt.');
                console.error('Błąd podczas pobierania wizyt:', err);
            }
        };

        fetchAppointments();
    }, [tab]);

    return (
        <div className="profile-history">
            <div className="tabs">
                <button
                    className={tab === 'upcoming' ? 'active' : ''}
                    onClick={() => setTab('upcoming')}
                >
                    Nadchodzące
                </button>
                <button
                    className={tab === 'history' ? 'active' : ''}
                    onClick={() => setTab('history')}
                >
                    Historia
                </button>
            </div>

            {error && <p className="error">{error}</p>}

            <div className="appointments">
                {appointments.length > 0 ? (
                    appointments.map((appointment) => {
                        const appointmentDate = new Date(appointment.date);
                        const dateString = appointmentDate.toLocaleDateString('pl-PL');
                        const timeString = appointmentDate.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit',
                        });

                        return (
                            <div key={appointment.id} className="appointment">
                                <p>
                                    <strong>Data:</strong> {dateString}
                                </p>
                                <p>
                                    <strong>Godzina:</strong> {timeString}
                                </p>
                                <p>
                                    <strong>Usługa:</strong>{' '}
                                    {appointment.service_name || 'Nie podano'}
                                </p>
                                <p>
                                    <strong>Fryzjer:</strong>{' '}
                                    {appointment.hairdresser_name || 'Dowolna osoba'}
                                </p>
                                {tab === 'history' && (
                                    <>
                                        <p>
                                            <strong>Status:</strong> {appointment.status || 'Nie podano'}
                                        </p>
                                        {/* Przycisk wysyłania faktury w odbytej wizycie */}
                                        <button
                                            className="invoice-button"
                                            onClick={() => handleSendInvoice(appointment.id)}
                                        >
                                            Wyślij fakturę na e-mail
                                        </button>
                                    </>
                                )}
                            </div>
                        );
                    })
                ) : (
                    <p className="no-visits">Brak wizyt do wyświetlenia</p>
                )}
            </div>
        </div>
    );
};

export default ProfileHistory;
