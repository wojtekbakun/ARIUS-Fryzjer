import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import axios from '../api/axios';
import './AppointmentPage.css';

const TimeSlotGroup = ({ label, slots, selectedTime, onSelectTime }) => {
    return (
        <div className="timeslot-group">
            <h4>{label}</h4>
            <div className="time-slots">
                {slots.length === 0 && <p className="no-slots">Brak dostępnych terminów</p>}
                {slots.map((slot) => (
                    <button
                        key={slot.time}
                        className={`time-slot ${
                            slot.available ? 'available' : 'unavailable'
                        } ${selectedTime === slot.time ? 'selected' : ''}`}
                        disabled={!slot.available}
                        onClick={() => onSelectTime(slot.time)}
                    >
                        {slot.time}
                    </button>
                ))}
            </div>
        </div>
    );
};

TimeSlotGroup.propTypes = {
    label: PropTypes.string.isRequired,
    slots: PropTypes.arrayOf(
        PropTypes.shape({
            time: PropTypes.string.isRequired,
            available: PropTypes.bool.isRequired,
        })
    ).isRequired,
    selectedTime: PropTypes.string.isRequired,
    onSelectTime: PropTypes.func.isRequired,
};

const AppointmentPage = () => {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedTime, setSelectedTime] = useState('');
    const [selectedService, setSelectedService] = useState('');
    const [selectedHairdresser, setSelectedHairdresser] = useState('');
    const [message, setMessage] = useState('');
    const [success, setSuccess] = useState(false);

    // Tablica, którą renderujemy w UI; zawiera pogrupowane sloty (rano, popołudnie, wieczór)
    const [availableSlots, setAvailableSlots] = useState([]);

    // Przykładowe usługi
    const services = [
        { id: 1, name: 'Strzyżenie damskie', price: 50 },
        { id: 2, name: 'Strzyżenie męskie', price: 40 },
        { id: 3, name: 'Koloryzacja', price: 120 },
        { id: 4, name: 'Modelowanie', price: 80 },
        { id: 5, name: 'Upięcia okolicznościowe', price: 150 },
        { id: 6, name: 'Inne', price: '---' },
    ];

    // Przykładowi fryzjerzy
    const hairdressers = [
        { id: 1, name: 'Jan Kowalski' },
        { id: 2, name: 'Michał Nowak' },
        { id: 3, name: 'Piotr Malinowski' },
        { id: 4, name: 'Anna Majewska' },
        { id: 5, name: 'Maria Nowicka' },
        { id: 6, name: 'Katarzyna Zielińska' },
        { id: 7, name: 'Magdalena Kwiatkowska' },
        { id: 8, name: 'Łukasz Wróbel' },
        { id: 9, name: 'Julia Wysocka' },
        { id: 10, name: 'Oliwia Dąbrowska' },
    ];

    /**
     * Funkcja zwracająca listę godzin (stringi "HH:MM") w zależności od dnia tygodnia.
     * 0 = niedziela  => brak godzin
     * 6 = sobota     => 9:00 - 18:00
     * 1..5 dni powszednie => 9:00 - 20:00
     */
    const getWorkingHours = (date) => {
        const day = date.getDay();
        if (day === 0) {
            return []; // niedziela
        }
        if (day === 6) {
            // sobota: 9:00–18:00
            return [
                '09:00', '10:00', '11:00', '12:00',
                '13:00', '14:00', '15:00', '16:00',
                '17:00', '18:00',
            ];
        }
        // poniedziałek–piątek: 9:00–20:00
        return [
            '09:00', '10:00', '11:00', '12:00',
            '13:00', '14:00', '15:00', '16:00',
            '17:00', '18:00', '19:00', '20:00',
        ];
    };

    /**
     * Główny efekt: za każdym razem, gdy zmieni się `selectedDate`,
     * pobieramy z backendu informację o już zajętych slotach i generujemy finalną listę dostępnych.
     */
    useEffect(() => {
        const fetchAndUpdate = async () => {
            try {
                // 1. Pobierz z backendu wszystkie wizyty, a następnie wyfiltruj te w danej dacie
                const response = await axios.get('/appointments/all');
                const bookedSlots = response.data
                    .filter((appointment) => {
                        const appDate = new Date(appointment.date);
                        return (
                            appDate.getFullYear() === selectedDate.getFullYear() &&
                            appDate.getMonth() === selectedDate.getMonth() &&
                            appDate.getDate() === selectedDate.getDate()
                        );
                    })
                    .map((appointment) => appointment.date.slice(11, 16));
                // to nam daje listę stringów "HH:MM", np. ["09:00", "10:00", ...]


                const workingHours = getWorkingHours(selectedDate);


                const groupedSlots = [
                    {
                        label: 'Rano (9:00 - 11:59)',
                        times: workingHours.filter((time) => time >= '09:00' && time < '12:00'),
                    },
                    {
                        label: 'Popołudnie (12:00 - 16:59)',
                        times: workingHours.filter((time) => time >= '12:00' && time < '17:00'),
                    },
                    {
                        label: 'Wieczór (17:00 - 20:00)',
                        times: workingHours.filter((time) => time >= '17:00' && time <= '20:00'),
                    },
                ];

                // Oznacz, które godziny są zajęte, a które wolne
                const finalSlots = groupedSlots.map((group) => ({
                    label: group.label,
                    slots: group.times.map((time) => ({
                        time,
                        available: !bookedSlots.includes(time),
                    })),
                }));

                // Ustaw stan - finalna tablica slotów do wyświetlenia
                setAvailableSlots(finalSlots);

                // Jeśli user zmienił datę, resetujemy ewentualnie wybraną godzinę
                setSelectedTime('');
            } catch (error) {
                console.error('Błąd pobierania / aktualizacji terminów:', error);
                setMessage('Wystąpił błąd podczas pobierania terminów.');
                setAvailableSlots([]);
            }
        };

        fetchAndUpdate();
        // Reset komunikatu sukcesu/błędu przy zmianie daty
        setSuccess(false);
        setMessage('');
    }, [selectedDate]);

    /**
     * Obsługa zmiany daty w kalendarzu
     */
    const handleDateChange = (date) => {
        setSelectedDate(date);
    };

    /**
     * Funkcja wywoływana po kliknięciu "Zarezerwuj"
     */
    const handleBooking = async () => {
        if (!selectedService || !selectedTime) {
            setMessage('Proszę wybrać usługę i godzinę.');
            setSuccess(false);
            return;
        }

        try {

            const userId = 1;
            const dateStr = selectedDate.toISOString().split('T')[0];
            const dateTimeStr = `${dateStr} ${selectedTime}:00`;

            const appointmentData = {
                service_id: parseInt(selectedService, 10),
                hairdresser_id: selectedHairdresser
                    ? parseInt(selectedHairdresser, 10)
                    : null,
                date: dateTimeStr,
            };


            await axios.post('/appointments', appointmentData, {
                headers: { 'Content-Type': 'application/json' },
            });

            setMessage('Wizyta została pomyślnie zarezerwowana!');
            setSuccess(true);
        } catch (error) {
            console.error('Błąd przy rezerwacji:', error);
            setMessage('Wystąpił błąd podczas rezerwacji.');
            setSuccess(false);
        }
    };

    return (
        <div className="appointment-page">
            <h2 className="page-title">Umów wizytę</h2>

            <div className="appointment-container">
                {/* Sekcja z kalendarzem */}
                <div className="calendar-section">
                    <label className="section-label">Wybierz datę:</label>
                    <Calendar
                        onChange={handleDateChange}
                        value={selectedDate}
                        minDate={new Date()}
                    />
                </div>

                {/* Sekcja z wyborem usługi, fryzjera i slotów */}
                <div className="reservation-details">
                    <div className="form-group">
                        <label>Wybierz usługę:</label>
                        <select
                            value={selectedService}
                            onChange={(e) => setSelectedService(e.target.value)}
                        >
                            <option value="">-- Wybierz usługę --</option>
                            {services.map((service) => (
                                <option key={service.id} value={service.id}>
                                    {service.name}{' '}
                                    {service.price !== '---' ? `(${service.price} PLN)` : ''}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Wybierz fryzjera:</label>
                        <select
                            value={selectedHairdresser}
                            onChange={(e) => setSelectedHairdresser(e.target.value)}
                        >
                            <option value="">Dowolna osoba</option>
                            {hairdressers.map((hd) => (
                                <option key={hd.id} value={hd.id}>
                                    {hd.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Sloty czasowe podzielone na grupy (rano / popołudnie / wieczór) */}
                    <div className="time-slot-container">
                        {availableSlots.map((group) => (
                            <TimeSlotGroup
                                key={group.label}
                                label={group.label}
                                slots={group.slots}
                                selectedTime={selectedTime}
                                onSelectTime={setSelectedTime}
                            />
                        ))}
                    </div>

                    <button onClick={handleBooking} className="book-button">
                        Zarezerwuj
                    </button>

                    {message && (
                        <p className={`message ${success ? 'success' : 'error'}`}>
                            {message}
                        </p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AppointmentPage;
