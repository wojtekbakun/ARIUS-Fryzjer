import React, { useState } from 'react';
import './ReviewsPage.css';

const ReviewsPage = () => {
    const [reviews, setReviews] = useState([
        { name: 'Anna Kowalska', rating: 5, comment: 'Świetna obsługa i piękne strzyżenie!' },
        { name: 'Jan Nowak', rating: 4, comment: 'Bardzo zadowolony, chociaż cena mogłaby być niższa.' },
    ]);
    const [newReview, setNewReview] = useState({ name: '', rating: 1, comment: '' });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewReview({ ...newReview, [name]: value });
    };

    const handleFormSubmit = (e) => {
        e.preventDefault();
        if (newReview.name && newReview.comment) {
            setReviews([...reviews, newReview]);
            setNewReview({ name: '', rating: 1, comment: '' });
        }
    };

    return (
        <div className="reviews-page">
            <h2>Oceny naszych klientów</h2>
            <div className="reviews-list">
                {reviews.map((review, index) => (
                    <div key={index} className="review-card">
                        <h3>{review.name}</h3>
                        <p>Ocena: {Array(review.rating).fill('⭐').join('')}</p>
                        <p>{review.comment}</p>
                    </div>
                ))}
            </div>
            <form className="review-form" onSubmit={handleFormSubmit}>
                <h3>Dodaj swoją opinię</h3>
                <input
                    type="text"
                    name="name"
                    placeholder="Twoje imię"
                    value={newReview.name}
                    onChange={handleInputChange}
                    required
                />
                <select
                    name="rating"
                    value={newReview.rating}
                    onChange={handleInputChange}
                    required
                >
                    {[1, 2, 3, 4, 5].map((num) => (
                        <option key={num} value={num}>{num}</option>
                    ))}
                </select>
                <textarea
                    name="comment"
                    placeholder="Twoja opinia"
                    value={newReview.comment}
                    onChange={handleInputChange}
                    required
                ></textarea>
                <button type="submit">Dodaj opinię</button>
            </form>
        </div>
    );
};

export default ReviewsPage;
