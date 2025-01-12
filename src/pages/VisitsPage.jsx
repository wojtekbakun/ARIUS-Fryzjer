import { useState, useEffect } from 'react';
import apiClient from '../api/axios';
import './VisitsPage.css';

const VisitsPage = () => {
    // Pełna lista wizyt zalogowanego użytkownika
    const [visits, setVisits] = useState([]);
    // Lista wizyt przefiltrowana w zależności od aktywnej zakładki
    const [filteredVisits, setFilteredVisits] = useState([]);
    const [activeTab, setActiveTab] = useState('upcoming'); // Domyślnie "Nadchodzące wizyty"
    const [error, setError] = useState('');

    // 1) Pierwszy efekt: pobieramy wizyty raz na start
    //    (lub zawsze, gdy potrzeba – możesz dostosować logikę).
    useEffect(() => {
        const fetchVisits = async () => {
            try {
                // wizyty zalogowanego usera, jeśli w nagłówku jest Bearer token.
                const response = await apiClient.get('/appointments');
                setVisits(response.data);
            } catch (err) {
                setError('Błąd podczas ładowania wizyt.');
                console.error('Błąd podczas pobierania wizyt:', err);
            }
        };

        fetchVisits();
    }, []);

    // 2) Drugi efekt: gdy zmienia się `activeTab` LUB `visits`,
    //    przefiltruj je i zapisz do `filteredVisits`.
    useEffect(() => {
        let filtered = [];
        if (activeTab === 'upcoming') {
            // Nadchodzące wizyty to te, gdzie data >= teraz
            filtered = visits.filter(
                (v) => new Date(v.date) >= new Date()
            );
        } else if (activeTab === 'completed') {
            // Zakończone wizyty: data < teraz
            filtered = visits.filter(
                (v) => new Date(v.date) < new Date()
            );
        }

        setFilteredVisits(filtered);
    }, [activeTab, visits]);

    const handleTabChange = (tab) => {
        setActiveTab(tab);
    };

    return (
        <div className="visits-page">
            <h2>Twoje wizyty</h2>

            <div className="tabs">
                <button
                    className={`tab ${activeTab === 'upcoming' ? 'active' : ''}`}
                    onClick={() => handleTabChange('upcoming')}
                >
                    Nadchodzące wizyty
                </button>
                <button
                    className={`tab ${activeTab === 'completed' ? 'active' : ''}`}
                    onClick={() => handleTabChange('completed')}
                >
                    Historia wizyt
                </button>
            </div>

            {error && <p className="error">{error}</p>}

            <div className="visits-list">
                {filteredVisits.length > 0 ? (
                    filteredVisits.map((visit) => {
                        const dateObj = new Date(visit.date);
                        const dateString = dateObj.toLocaleDateString('pl-PL');
                        const timeString = dateObj.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit',
                        });
                        return (
                            <div key={visit.id} className="visit-card">
                                <h3>{visit.service_name || 'Nie podano usługi'}</h3>
                                <p>Data: {dateString}</p>
                                <p>Godzina: {timeString}</p>
                                <p>
                                    Status:{' '}
                                    {new Date(visit.date) >= new Date()
                                        ? 'Nadchodząca'
                                        : 'Zakończona'}
                                </p>
                                {/* Możesz też użyć visit.status z backendu, jeśli tam jest. */}
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

export default VisitsPage;
