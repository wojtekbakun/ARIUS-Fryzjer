import "react";
import './ServicesPage.css';

const ServicesPage = () => {
    const services = [
        {
            id: 1,
            name: "Strzyżenie damskie",
            description: "Precyzyjne strzyżenie, które podkreśli Twoją urodę.",
            price: "od 50 PLN"
        },
        {
            id: 2,
            name: "Strzyżenie męskie",
            description: "Klasyczne lub nowoczesne cięcie dostosowane do Twoich potrzeb.",
            price: "od 40 PLN"
        },
        {
            id: 3,
            name: "Koloryzacja",
            description: "Najmodniejsze odcienie i techniki koloryzacji, które ożywią Twój wygląd.",
            price: "od 120 PLN"
        },
        {
            id: 4,
            name: "Modelowanie",
            description: "Stylizacja, która doda Twoim włosom objętości i blasku.",
            price: "od 80 PLN"
        },
        {
            id: 5,
            name: "Upięcia okolicznościowe",
            description: "Eleganckie upięcia na każdą okazję, które przyciągną spojrzenia.",
            price: "od 150 PLN"
        }
    ];

    return (
        <section className="services-page">
            <div className="services-header">
                <h2>Nasze usługi</h2>
                <p>
                    Oferujemy szeroki zakres usług fryzjerskich, które spełnią oczekiwania najbardziej wymagających klientów.
                </p>
            </div>
            <div className="services-list">
                {services.map((service) => (
                    <div key={service.id} className="service-item">
                        <h3>{service.name}</h3>
                        <p className="service-description">{service.description}</p>
                        <p className="service-price">{service.price}</p>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default ServicesPage;
