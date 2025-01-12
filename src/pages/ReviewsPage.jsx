import { useState, useEffect } from 'react';
import apiClient from '../api/axios';
import './ReviewsPage.css';

const ReviewsPage = () => {
    const [reviews, setReviews] = useState([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await apiClient.get('/reviews');
                setReviews(response.data);
            } catch (err) {
                console.error('Błąd podczas pobierania opinii:', err);
                setMessage('Wystąpił błąd podczas pobierania opinii.');
            }
        };

        fetchReviews();
    }, []);

    return (
        <div className="reviews-page">
            <h2>Oceny naszych klientów</h2>
            {message && <p className="error-message">{message}</p>}
            <div className="reviews-list">
                {reviews.length > 0 ? (
                    reviews.map((review, index) => (
                        <div key={index} className="review-card">
                            <h3>{review.user_name || 'Anonimowy'}</h3>
                            <p>Ocena: {Array(review.rating).fill('⭐').join('')}</p>
                            <p>{review.comment || 'Brak komentarza.'}</p>
                        </div>
                    ))
                ) : (
                    <p>Brak opinii do wyświetlenia.</p>
                )}
            </div>
        </div>
    );
};

export default ReviewsPage;
