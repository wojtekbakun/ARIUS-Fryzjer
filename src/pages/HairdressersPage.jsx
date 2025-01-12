import 'react';
import './HairdressersPage.css';

const hairdressers = [
    {
        name: 'Jan Kowalski',
        description: 'Specjalista od nowoczesnych fryzur męskich i brody. Zawsze dostosowuje fryzury do charakteru klienta.',
        photo: '/guy1 (1).jpg',
    },
    {
        name: 'Michał Nowak',
        description: 'Ekspert od klasycznego strzyżenia i stylizacji. Uwielbia wprowadzać świeżość w klasyczne cięcia.',
        photo: '/guy2 (1).jpg',
    },
    {
        name: 'Piotr Malinowski',
        description: 'Fryzjer z 10-letnim doświadczeniem, pasjonat koloryzacji. Specjalizuje się w odważnych metamorfozach.',
        photo: '/guy3 (1).jpg',
    },
    {
        name: 'Anna Majewska',
        description: 'Mistrzyni upięć ślubnych i okolicznościowych. Potrafi stworzyć fryzurę, która przetrwa każdą uroczystość.',
        photo: '/girl1 (1).jpg',
    },
    {
        name: 'Maria Nowicka',
        description: 'Specjalistka od stylizacji i regeneracji włosów. Stawia na naturalne metody pielęgnacji.',
        photo: '/girl2 (1).jpg',
    },
    {
        name: 'Katarzyna Zielińska',
        description: 'Ekspertka od koloryzacji i pielęgnacji włosów. Uwielbia eksperymentować z nowymi technikami farbowania.',
        photo: '/girl3 (1).jpg',
    },
    {
        name: 'Magdalena Kwiatkowska',
        description: 'Artystka fryzjerstwa z międzynarodowym doświadczeniem. Specjalizuje się w stylizacjach awangardowych.',
        photo: '/girl4 (1).jpg',
    },
    {
        name: 'Łukasz Wróbel',
        description: 'Mistrz precyzyjnych strzyżeń i stylizacji. Zawsze dba o każdy szczegół.',
        photo: '/guy4 (1).jpg',
    },
    {
        name: 'Julia Wysocka',
        description: 'Pasjonatka koloryzacji ombre i balayage. Znana z kreatywności i unikalnych efektów.',
        photo: '/girl5 (1).jpg',
    },
    {
        name: 'Oliwia Dąbrowska',
        description: 'Specjalistka od regeneracji włosów i zabiegów pielęgnacyjnych. Zawsze stawia na zdrowie włosów swoich klientów.',
        photo: '/girl6 (1).jpg',
    },
];

const HairdressersPage = () => {
    return (
        <div className="hairdressers-container">
            <h1>Nasi Fryzjerzy</h1>
            <div className="hairdressers-grid">
                {hairdressers.map((hairdresser, index) => (
                    <div key={index} className="hairdresser-card">
                        <img
                            src={hairdresser.photo}
                            alt={`Zdjęcie ${hairdresser.name}`}
                            className="hairdresser-photo"
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
