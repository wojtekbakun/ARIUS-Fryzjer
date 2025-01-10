import React, { useState, useEffect } from 'react';
import ProfileData from './ProfileData';
import ProfileHistory from './ProfileHistory';
import ProfileReviews from './ProfileReviews';
import './ProfilePage.css';

const ProfilePage = () => {
    const [activeTab, setActiveTab] = useState('data');

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/login';
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login';
    };

    return (
        <div className="profile-page">
            <h1>Twój Profil</h1>
            <nav className="profile-nav">
                <button onClick={() => setActiveTab('data')} className={activeTab === 'data' ? 'active' : ''}>Dane</button>
                <button onClick={() => setActiveTab('history')} className={activeTab === 'history' ? 'active' : ''}>Wizyty</button>
                <button onClick={() => setActiveTab('reviews')} className={activeTab === 'reviews' ? 'active' : ''}>Oceny</button>
            </nav>
            <div className="profile-content">
                {activeTab === 'data' && <ProfileData />}
                {activeTab === 'history' && <ProfileHistory />}
                {activeTab === 'reviews' && <ProfileReviews />}
            </div>
            <button className="logout-button" onClick={handleLogout}>Wyloguj</button>
        </div>
    );
};

export default ProfilePage;
