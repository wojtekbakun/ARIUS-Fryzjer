import React from 'react';
import './HomePage.css';

const HomePage = () => {
    const reasons = [
        {
            imgSrc: '/img1.jpg',
            title: 'SLOW HAIR',
            description: 'Od zawsze w naszym salonie klientami zajmuje się jedna osoba, która poświęca Ci 100% uwagi. Jako pierwsi użyliśmy hasła "slow hair".',
        },
        {
            imgSrc: '/img2.jpg',
            title: 'INKLUZYWNOŚĆ',
            description: 'Zgodnie z naszym przesłaniem "Bądź sobą" chcemy, aby każdy czuł się komfortowo i bezpiecznie. Nasz cennik jest niezależny od płci.',
        },
        {
            imgSrc: '/img3.jpg',
            title: 'DOŚWIADCZENIE',
            description: 'Kadra naszych fryzjerów posiada różnorodne doświadczenia, dlatego na pewno znajdziesz kogoś idealnego dla swoich potrzeb.',
        },
        {
            imgSrc: '/img4.jpg',
            title: 'RELAX W PRACY',
            description: 'W trakcie wizyty delektuj się naszą kawą, herbatą lub przekąskami. Możesz też pracować zdalnie w spokoju.',
        },
        {
            imgSrc: '/img5.jpg',
            title: 'ŁATWOŚĆ PLANOWANIA',
            description: 'U nas nie ma kolejek! Wszystkie wizyty realizujemy na czas, w dogodnym dla Ciebie terminie.',
        },
        {
            imgSrc: '/img6.jpg',
            title: 'PROFESJONALIZM',
            description: 'Stawiamy na najwyższą jakość usług, aby spełnić Twoje oczekiwania.',
        },
    ];

    return (
        <div>
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <h1>fryzjerski<sup>®</sup></h1>
                    <p>Profesjonalne usługi fryzjerskie na najwyższym poziomie</p>
                    <a className="cta-button" href="#appointment">Umów wizytę</a>
                </div>
            </section>

            {/* About Section */}
            <section className="about" id="about">
                <h2>Witamy w naszym salonie</h2>
                <p>
                    Jesteśmy salonem fryzjerskim z wieloletnim doświadczeniem. Oferujemy profesjonalne koloryzacje,
                    dopracowane strzyżenia i stylizacje na każdą okazję.
                </p>
            </section>

            {/* Reasons Section */}
            <section className="reasons-section">
                <h2>Dlaczego warto nas wybrać?</h2>
                <div className="reasons-container">
                    {reasons.map((reason, index) => (
                        <div className="reason-card" key={index}>
                            <img src={reason.imgSrc} alt={reason.title} />
                            <h3>{reason.title}</h3>
                            <p>{reason.description}</p>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default HomePage;
