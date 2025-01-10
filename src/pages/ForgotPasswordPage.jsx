import React from 'react';

const HairdressersPage = () => {
    const hairdressers = [
        { id: 1, name: 'Anna Kowalska', description: 'Specjalistka od koloryzacji i strzyżenia.', photo: '/images/anna.jpg' },
        { id: 2, name: 'Jan Nowak', description: 'Ekspert w męskich fryzurach.', photo: '/images/jan.jpg' },
        { id: 3, name: 'Katarzyna Malinowska', description: 'Mistrzyni upięć okolicznościowych.', photo: '/images/katarzyna.jpg' },
    ];

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <h2>Nasi Fryzjerzy</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
                {hairdressers.map((hairdresser) => (
                    <div
                        key={hairdresser.id}
                        style={{
                            border: '1px solid #ddd',
                            borderRadius: '5px',
                            padding: '1rem',
                            width: '250px',
                            textAlign: 'center',
                        }}
                    >
                        <img
                            src={hairdresser.photo}
                            alt={hairdresser.name}
                            style={{ width: '100%', borderRadius: '5px' }}
                        />
                        <h3>{hairdresser.name}</h3>
                        <p>{hairdresser.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HairdressersPage;
