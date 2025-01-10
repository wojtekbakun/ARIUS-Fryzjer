import React, { useState } from 'react';
import Calendar from 'react-calendar'; // Kalendarz
import 'react-calendar/dist/Calendar.css'; // Style dla kalendarza

const AppointmentPage = () => {
    const [selectedService, setSelectedService] = useState('');
    const [selectedHairdresser, setSelectedHairdresser] = useState('');
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedTime, setSelectedTime] = useState('');
    const [comment, setComment] = useState('');
    const [message, setMessage] = useState('');

    // Lista usług
    const services = [
        { id: 1, name: 'Strzyżenie damskie od', price: 50 },
        { id: 2, name: 'Strzyżenie męskie od', price: 40 },
        { id: 3, name: 'Koloryzacja od', price: 120 },
        { id: 4, name: 'Modelowanie od', price: 80 },
        { id: 5, name: 'Upięcia okolicznościowe od', price: 150 },
        { id: 6, name: 'Inne', price: '---' },
    ];

    // Lista fryzjerów
    const hairdressers = [
        { id: 1, name: 'Anna Kowalska' },
        { id: 2, name: 'Jan Nowak' },
        { id: 3, name: 'Katarzyna Malinowska' },
        { id: 4, name: 'Piotr Wróblewski' },
        { id: 5, name: 'Ewa Zawadzka' },
        { id: 6, name: 'Magdalena Wiśniewska' },
        { id: 7, name: 'Michał Dąbrowski' },
        { id: 8, name: 'Karolina Nowicka' },
        { id: 9, name: 'Tomasz Zieliński' },
        { id: 10, name: 'Joanna Wiśniewska' },
    ];

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!selectedService || !selectedHairdresser || !selectedDate || !selectedTime) {
            setMessage('Proszę wypełnić wszystkie pola.');
            return;
        }

        // Symulacja wysyłki danych
        console.log('Rezerwacja:', {
            service: selectedService,
            hairdresser: selectedHairdresser,
            date: selectedDate.toISOString().split('T')[0],
            time: selectedTime,
            comment,
        });

        setMessage('Wizyta została umówiona pomyślnie!');
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto', background: '#f8f8f8', borderRadius: '10px' }}>
            <h2 style={{ textAlign: 'center', marginBottom: '1rem', color: '#333' }}>Umów wizytę</h2>
            {message && (
                <p style={{ color: message.includes('błąd') ? 'red' : 'green', textAlign: 'center' }}>{message}</p>
            )}
            <form onSubmit={handleSubmit}>
                {/* Wybór usługi */}
                <label>
                    Wybierz usługę:
                    <select
                        value={selectedService}
                        onChange={(e) => setSelectedService(e.target.value)}
                        required
                        style={{ display: 'block', width: '100%', padding: '0.5rem', margin: '1rem 0', borderRadius: '5px' }}
                    >
                        <option value="">-- Wybierz usługę --</option>
                        {services.map((service) => (
                            <option key={service.id} value={service.name}>
                                {service.name} - {service.price} PLN
                            </option>
                        ))}
                    </select>
                </label>

                {/* Wybór fryzjera */}
                <label>
                    Wybierz fryzjera:
                    <select
                        value={selectedHairdresser}
                        onChange={(e) => setSelectedHairdresser(e.target.value)}
                        required
                        style={{ display: 'block', width: '100%', padding: '0.5rem', margin: '1rem 0', borderRadius: '5px' }}
                    >
                        <option value="">-- Wybierz fryzjera --</option>
                        {hairdressers.map((hairdresser) => (
                            <option key={hairdresser.id} value={hairdresser.name}>
                                {hairdresser.name}
                            </option>
                        ))}
                    </select>
                </label>

                {/* Wybór daty */}
                <label>
                    Wybierz datę:
                    <Calendar
                        onChange={setSelectedDate}
                        value={selectedDate}
                        style={{ marginBottom: '1rem' }}
                    />
                </label>

                {/* Wybór godziny */}
                <label>
                    Wybierz godzinę:
                    <input
                        type="time"
                        value={selectedTime}
                        onChange={(e) => setSelectedTime(e.target.value)}
                        required
                        style={{ display: 'block', width: '100%', padding: '0.5rem', margin: '1rem 0', borderRadius: '5px' }}
                    />
                </label>

                {/* Komentarz */}
                <label>
                    Dodaj komentarz (opcjonalnie):
                    <textarea
                        value={comment}
                        onChange={(e) => setComment(e.target.value)}
                        placeholder="Wpisz tutaj dodatkowe uwagi..."
                        style={{ display: 'block', width: '100%', padding: '0.5rem', margin: '1rem 0', borderRadius: '5px' }}
                    />
                </label>

                {/* Przycisk zatwierdzający */}
                <button
                    type="submit"
                    style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: '#333',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        width: '100%',
                    }}
                >
                    Umów wizytę
                </button>
            </form>
        </div>
    );
};

export default AppointmentPage;
