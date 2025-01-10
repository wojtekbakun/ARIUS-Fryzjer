import React, { useState, useEffect } from 'react';

const ProfileReviews = () => {
    const [reviews, setReviews] = useState([]);
    const [newReview, setNewReview] = useState({ hairdresserId: '', rating: 1, comment: '' });

    useEffect(() => {
        // Pobierz istniejące oceny
        fetch('/api/reviews')
            .then((res) => res.json())
            .then((data) => setReviews(data));
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewReview({ ...newReview, [name]: value });
    };

    const handleFormSubmit = (e) => {
        e.preventDefault();
        // Wyślij nową ocenę do backendu
        console.log('Wysłano ocenę:', newReview);
    };

    return (
        <div className="profile-reviews">
            <h2>Oceny</h2>
            <ul>
                {reviews.map((review) => (
                    <li key={review.id}>
                        <p>Fryzjer: {review.hairdresser}</p>
                        <p>Ocena: {review.rating} ⭐</p>
                        <p>Komentarz: {review.comment}</p>
                    </li>
                ))}
            </ul>
            <form onSubmit={handleFormSubmit}>
                <label>
                    Fryzjer:
                    <input type="text" name="hairdresserId" value={newReview.hairdresserId} onChange={handleInputChange} required />
                </label>
                <label>
                    Ocena:
                    <select name="rating" value={newReview.rating} onChange={handleInputChange} required>
                        {[1, 2, 3, 4, 5].map((num) => (
                            <option key={num} value={num}>{num} ⭐</option>
                        ))}
                    </select>
                </label>
                <label>
                    Komentarz:
                    <textarea name="comment" value={newReview.comment} onChange={handleInputChange} required></textarea>
                </label>
                <button type="submit">Dodaj opinię</button>
            </form>
        </div>
    );
};

export default ProfileReviews;
