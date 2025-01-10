import React, { useEffect, useState } from 'react';

const ProfileHistory = () => {
    const [history, setHistory] = useState([]);
    const [upcoming, setUpcoming] = useState([]);

    useEffect(() => {
        fetch('/api/history')
            .then((res) => res.json())
            .then((data) => setHistory(data));

        fetch('/api/upcoming')
            .then((res) => res.json())
            .then((data) => setUpcoming(data));
    }, []);

    return (
        <div className="profile-history">
            <h2>Historia wizyt</h2>
            <ul>
                {history.map((item) => (
                    <li key={item.id}>
                        <p>Data: {item.date}</p>
                        <p>Usługa: {item.service}</p>
                        <p>Fryzjer: {item.hairdresser}</p>
                    </li>
                ))}
            </ul>
            <h2>Nadchodzące wizyty</h2>
            <ul>
                {upcoming.map((item) => (
                    <li key={item.id}>
                        <p>Data: {item.date}</p>
                        <p>Usługa: {item.service}</p>
                        <p>Fryzjer: {item.hairdresser}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProfileHistory;
